from abc import ABC

import pygame
import numpy as np

from NudWar.game.region import Region
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.nud import Nud
from NudWar.game.portal import Portal

from NudWar.manager.mapManager import MapManager

from NudWar.render.window import Window
from NudWar.utils.pumpy import *

from NudWar.data.unitData import UnitData
from NudWar.data.renderData import *

from NudWar.game.transformGameObject import TransformGameObject

from NudWar.data.mapData import MapData

class Renderer:
	"""
	Technically a manager but is currently categorized in the rendering folder. May change.
	"""
	def __init__(self):
		self.map: Map = None
		self.window: Window = None
		self.camera: Camera = None
		self.mapManager: MapManager = None
		
		self.unitData: UnitData = None
		self.renderData: RenderData = None
		self.mapData: MapData = None

	def ImportModules(self, map: Map, window: Window, camera: Camera, mapManager: MapManager):
		self.map = map
		self.window = window
		self.camera = camera
		self.mapManager = mapManager

	def ImportData(self, unitData: UnitData, renderData: RenderData, mapData: MapData):
		self.unitData = unitData
		self.renderData = renderData
		self.mapData = mapData
	
	def ToGameSpace(self, vertices: list[list[float, float]], region: Region, transform: TransformGameObject):
		for  i, vertex in enumerate(vertices):
			vertex = MultiplyVectors(vertex, transform.rot)
			vertex[0] *= transform.GetW()
			vertex[1] *= transform.GetH()
			vertex[0] += transform.GetX()
			vertex[1] += transform.GetY()
			vertex[0] += region.GetX()
			vertex[1] += region.GetY()

			vertices[i] = vertex

	def ToScreenSpace(self, vertices: list[list[float, float]]):
		center = self.window.GetCenter()
		for vertex in vertices:
			vertex[0] -= self.camera.GetX()
			vertex[1] -= self.camera.GetY()
			vertex[0] *= self.camera.GetW()
			vertex[1] *= self.camera.GetH()

			vertex[0] += center[0]
			vertex[1] += center[1]

	def RenderTopLeftBox(self, rect: tuple, color: tuple[int], rectWidth: int = 0):
		"""
		
		'Top-Left box' means that the coordinates of the box are at the top left.
		
		rect coordinates are in game space and the function transfers it to screen space

		"""
		center = self.window.GetCenter()

		pygame.draw.rect(
			self.window.GetInstance(),
			color,
			(
				(
					rect[0] - self.camera.pos[0]) * self.camera.scale[0] + center[0],
					(rect[1] - self.camera.pos[1]) * self.camera.scale[1] + center[1],
					rect[2] * self.camera.scale[0],
					rect[3] * self.camera.scale[1]
			),
			rectWidth
		)
	
	def RenderSimpleNud(self, nud: Nud, region: Region, color: tuple[int] = (255, 255, 255)):
		vertices = self.renderData.basicNudPrefab.GetMesh()

		self.ToGameSpace(vertices, region, nud)
		self.ToScreenSpace(vertices)
		
		pygame.draw.polygon(self.window.GetInstance(), color, vertices)

	def RenderPortal(self, portal: Portal, region: Region):
		mesh = self.renderData.portalPrefab.GetMesh()
		self.ToGameSpace(mesh, region, portal)
		self.ToScreenSpace(mesh)

		center = [[0, 0]]

		self.ToGameSpace(center, region, portal)
		self.ToScreenSpace(center)
		center = center[0]

		pygame.draw.polygon(self.window.GetInstance(), self.renderData.portalPrefab.PORTAL_TENDRIL_COLOR, mesh)
		pygame.draw.circle(self.window.GetInstance(), self.renderData.portalPrefab.PORTAL_EPICENTER_COLOR, center, self.renderData.portalPrefab.PORTAL_EPICENTER_RADIUS * portal.GetW() * self.camera.GetW())

	def FillBackground(self, color: tuple):
		self.window.GetInstance().fill(color)

	def GridRegionRender(self, region: Region):
		"""
		Renders the borders of a region in a white box.
		"""
		self.RenderTopLeftBox(
			(region.pos[0], region.pos[1], region.scale[0], region.scale[1]),
			(255, 255, 255),
			1
		)

	def RenderRegion(self, region: Region):
		"""
		
		Entry method for rendering a region. This includes the rendering of all objects within the region.
		
		"""
		self.GridRegionRender(region)

		objects = list(region.objects)

		for index, object in reversed(list(enumerate(objects))):
			if isinstance(object, Portal):
				self.RenderPortal(object, region)
				objects.pop(index)

		for index, object in reversed(list(enumerate(objects))):
			if isinstance(object, Nud):
				self.RenderSimpleNud(object, region)
				objects.pop(index)

	def FixedUpdate(self):
		self.renderData.portalPrefab.FixedUpdate()
	
	def Update(self):
		self.FillBackground((50, 50, 50))

		for region in self.mapManager.GetAllRegions():
			self.RenderRegion(region)

		pygame.display.flip()