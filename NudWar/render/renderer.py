from abc import ABC

import pygame
import numpy as np

from NudWar.game.region import Region
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.nud import Nud
from NudWar.render.window import Window

class Renderer:
	"""
	Technically a manager but is currently categorized in the rendering folder. May change.
	"""
	def __init__(self, map: Map, window: Window, camera: Camera):
		self.map = map
		self.window = window
		self.camera = camera

	def ToScreenSpace(self, vertex: list[float]) -> list[float]:
		"""
		Takes a vertex and transforms it from game space to screen space.
		"""

		outputVertex = [vertex[0], vertex[1]]

		outputVertex[0] -= self.camera.GetX()
		outputVertex[1] -= self.camera.GetY()
		outputVertex[0] *= self.camera.GetW()
		outputVertex[1] *= self.camera.GetH()

		center = self.window.GetCenter()

		outputVertex[0] += center[0]
		outputVertex[1] += center[1]

		return outputVertex

	def RenderTopLeftBox(self, rect: tuple, color: tuple[int], rectWidth: int = 0):
		"""
		
		'Top-Left box' means that the coordinates of the box are at the top left.
		
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
		vertices = [
			[-0.30, -0.25],
			[0.35, 0.0],
			[-0.30, 0.25],
			[-0.10, 0.0]
		]

		for i in range(0, len(vertices), 1):
			outputVertex = nud.ToGameSpace(vertices[i])
			vertices[i][0] = outputVertex[0]
			vertices[i][1] = outputVertex[1]
			outputVertex = self.ToScreenSpace(vertices[i])
			vertices[i][0] = outputVertex[0]
			vertices[i][1] = outputVertex[1]
		
		pygame.draw.polygon(self.window.GetInstance(), color, vertices)

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
	
	def Update(self):
		self.FillBackground((50, 50, 50))

		for region in self.map.GetAllRegions():
			self.RenderRegion(region)

		pygame.display.flip()