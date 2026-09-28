from abc import ABC

import pygame
import numpy as np

from NudWar.game.region import Region
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.nud import Nud
from NudWar.game.portal import Portal

from NudWar.render.window import Window
from NudWar.utils.pumpy import *

from NudWar.data.unitData import UnitData
from NudWar.data.renderData import RenderData

from NudWar.game.transformGameObject import TransformGameObject

class Renderer:
	"""
	Technically a manager but is currently categorized in the rendering folder. May change.
	"""
	def __init__(self):
		self.map: Map = None
		self.window: Window = None
		self.camera: Camera = None
		
		self.unitData: UnitData = None
		self.renderData: RenderData = None

		# portal prefab data
		self.portalCWRotation = [1.0, 0.0]
		self.portalCCWRotation = [0.0, 1.0]

	def ImportModules(self, map: Map, window: Window, camera: Camera):
		self.map = map
		self.window = window
		self.camera = camera

	def ImportData(self, unitData: UnitData, renderData: RenderData):
		self.unitData = unitData
		self.renderData = renderData
	
	def ToGameSpace(self, vertices: list[list[float, float]], transform: TransformGameObject):
		for  i, vertex in enumerate(vertices):
			vertex = MultiplyVectors(vertex, transform.rot)
			vertex[0] *= transform.GetW()
			vertex[1] *= transform.GetH()
			vertex[0] += transform.GetX()
			vertex[1] += transform.GetY()

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
	
	def RenderSimpleNud(self, nud: Nud, color: tuple[int] = (255, 255, 255)):
		vertices = self.renderData.GetBasicNudMesh()

		self.ToGameSpace(vertices, nud)
		self.ToScreenSpace(vertices)
		
		pygame.draw.polygon(self.window.GetInstance(), color, vertices)

	def RenderPortal(self, portal: Portal):
		cwTendrilVertices = self.renderData.GetPortalTendril()
		ccwTendrilVertices = self.renderData.GetPortalTendril()

		for i, vertex in enumerate(cwTendrilVertices):
			vertex = MultiplyVectors(vertex, self.portalCWRotation)
			cwTendrilVertices[i] = vertex
		
		for i, vertex in enumerate(ccwTendrilVertices):
			vertex = MultiplyVectors(vertex, self.portalCCWRotation)
			ccwTendrilVertices[i] = vertex

		self.ToGameSpace(cwTendrilVertices, portal)
		self.ToScreenSpace(cwTendrilVertices)

		self.ToGameSpace(ccwTendrilVertices, portal)
		self.ToScreenSpace(ccwTendrilVertices)

		otherData = [[0, 0]]
		self.ToGameSpace(otherData, portal)
		self.ToScreenSpace(otherData)
		centerCoordinate = otherData[0]

		pygame.draw.polygon(self.window.GetInstance(), (112, 41, 41), cwTendrilVertices)
		pygame.draw.polygon(self.window.GetInstance(), (31, 14, 145), ccwTendrilVertices)
		pygame.draw.circle(self.window.GetInstance(), (180, 180, 180), centerCoordinate, self.renderData.PORTAL_EPICENTER_RADIUS * portal.GetW() * self.camera.GetW())


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

		for object in region.objects:
			if isinstance(object, Nud):
				self.RenderSimpleNud(object)

	def FixedUpdate(self):
		self.portalCWRotation = MultiplyVectors(self.portalCWRotation, self.renderData.PORTAL_CW_TENDRIL_VECTOR)
		self.portalCWRotation = normalizeVector(self.portalCWRotation)
		self.portalCCWRotation = MultiplyVectors(self.portalCCWRotation, self.renderData.PORTAL_CCW_TENDRIL_VECTOR)
		self.portalCCWRotation = normalizeVector(self.portalCCWRotation)
	
	def Update(self):
		self.FillBackground((50, 50, 50))

		portal = Portal()
		portal.pos = [30, 40]
		self.RenderPortal(portal)

		for region in self.map.GetAllRegions():
			self.RenderRegion(region)

		pygame.display.flip()