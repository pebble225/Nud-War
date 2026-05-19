from abc import ABC

import pygame

from NudWar.game.region import Region
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.render.window import Window

class Renderer:
	def __init__(self, map: Map, window: Window, camera: Camera):
		self.map = map
		self.window = window
		self.camera = camera

	def TransformVertex(self, vertex: list[float]):
		"""
		Takes a vertex and transforms it from game space to screen space.
		"""

		vertex[0] -= self.camera.GetX()
		vertex[1] -= self.camera.GetY()
		vertex[0] *= self.camera.GetW()
		vertex[1] *= self.camera.GetH()

		center = self.window.GetCenter()

		vertex[0] += center[0]
		vertex[1] += center[1]

	def RenderCornerBox(self, rect: tuple, color: tuple[int], rectWidth: int = 0):
		vertices = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]

		for vertex in vertices:
			vertex[0] *= rect[2]
			vertex[1] *= rect[3]
			vertex[0] += rect[0]
			vertex[1] += rect[1]

			self.TransformVertex(vertex)
		
		pygame.draw.rect(
			self.window.GetInstance(),
			color,
			(
				vertices[0][0], vertices[0][1], vertices[1][0]-vertices[0][0], vertices[2][1]-vertices[0][1]
			),
			rectWidth
		)

	def FillBackground(self, color: tuple):
		self.window.GetInstance().fill(color)

	def GridRegionRender(self, region: Region):
		self.RenderCornerBox(
			(region.pos[0], region.pos[1], region.scale[0], region.scale[1]),
			(255, 255, 255),
			1
		)

	def RenderRegion(self, region: Region):
		self.GridRegionRender(region)
	
	def Update(self):
		self.FillBackground((50, 50, 50))

		for region in self.map.GetAllRegions():
			self.RenderRegion(region)

		pygame.display.flip()