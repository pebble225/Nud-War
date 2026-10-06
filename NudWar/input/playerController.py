from NudWar.game.transformGameObject import TransformGameObject
from NudWar.game.camera import Camera

import pygame
from pygame.locals import *

class PlayerController:
	def __init__(self):
		self.UP = False
		self.DOWN = False
		self.LEFT = False
		self.RIGHT = False

		self.clearScrollEvent = False
		self.SCROLL_EVENT: int | None = None

		self.target: TransformGameObject = None
	
	def RegisterEvent(self, e: pygame.event):
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_w or e.key == pygame.K_UP:
				self.UP = True
			elif e.key == pygame.K_s or e.key == pygame.K_DOWN:
				self.DOWN = True
			if e.key == pygame.K_a or e.key == pygame.K_LEFT:
				self.LEFT = True
			elif e.key == pygame.K_d or e.key == pygame.K_RIGHT:
				self.RIGHT = True
		elif e.type == pygame.KEYUP:
			if e.key == pygame.K_w or e.key == pygame.K_UP:
				self.UP = False
			elif e.key == pygame.K_s or e.key == pygame.K_DOWN:
				self.DOWN = False
			if e.key == pygame.K_a or e.key == pygame.K_LEFT:
				self.LEFT = False
			elif e.key == pygame.K_d or e.key == pygame.K_RIGHT:
				self.RIGHT = False
		elif e.type == pygame.MOUSEWHEEL:
			if e.y != 0:
				self.SCROLL_EVENT = e.y


	def GetUp(self) -> bool:
		return self.UP
	
	def GetDown(self) -> bool:
		return self.DOWN
	
	def GetLeft(self) -> bool:
		return self.LEFT
	
	def GetRight(self) -> bool:
		return self.RIGHT
	
	def GetForward(self) -> bool:
		return self.UP
	
	def GetBackward(self) -> bool:
		return self.DOWN

	def GetScrollEvent(self) -> int | None:
		self.clearScrollEvent = True

		return self.SCROLL_EVENT

	def ClearScrollEvent(self):
		if self.clearScrollEvent:
			self.clearScrollEvent = False
			self.SCROLL_EVENT = None

	def Update(self):
		#0.707106

		if isinstance(self.target, Camera):
			if self.GetUp():
				self.target.NudgeCamera(0.0, -1.0)
			elif self.GetDown():
				self.target.NudgeCamera(0.0, 1.0)
			
			if self.GetLeft():
				self.target.NudgeCamera(-1.0, 0.0)
			elif self.GetRight():
				self.target.NudgeCamera(1.0, 0.0)
			
			scroll = self.GetScrollEvent()
			if scroll is not None:
				if scroll > 0:
					self.target.scale[0] *= 2
					self.target.scale[1] *= 2
					self.target.moveSpeed = self.target.moveSpeed / 2
				elif scroll < 0:
					self.target.scale[0] /= 2
					self.target.scale[1] /= 2
					self.target.moveSpeed *= 2

	
	def SetTarget(self, target: TransformGameObject):
		self.target = target