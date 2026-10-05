from NudWar.game.gameObject import GameObject
from NudWar.utils.pumpy import *
import math
import numpy as np

class TransformGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.pos = [0.0, 0.0]
		self.rot = [1.0, 0.0]
		self.scale = [1.0, 1.0]
		self.collisionBoxDim = [1.0, 1.0]
		self.renderObject = None

		self.name = None # this is meant for debugging. It allows the Player Controller to provide special input behavior
	
	def GetX(self) -> float:
		return self.pos[0]

	def GetY(self) -> float:
		return self.pos[1]
	
	def GetPosition(self) -> list:
		return self.pos.copy()
	
	def GetPositionPlusOffet(self, offset: list[float, float]) -> list:
		return [self.pos[0] + offset[0], self.pos[1] + offset[1]]
	
	def SetPosition(self, x: float, y: float):
		self.pos[0] = x
		self.pos[1] = y
	
	def SetPosition2(self, pos: list[float, float]):
		self.pos[0] = pos[0]
		self.pos[1] = pos[1]
	
	def GetW(self) -> float:
		return self.scale[0]

	def GetH(self) -> float:
		return self.scale[1]
	
	def GetScale(self) -> list:
		return self.scale.copy()
	
	def SetScale(self, w: float, h: float = None):
		if h is None:
			self.scale[0] = w
			self.scale[1] = w
		else:
			self.scale[0] = w
			self.scale[1] = h

	def IsWithinDistanceTo(self, obj: "TransformGameObject", tolerance: float = 1) -> bool:
		"""
		@param tolerance distance in meters
		"""
		return not (distanceFormula(self.pos, obj.pos) > tolerance)

	def GetRotationAngle(self) -> float:
		return math.degrees(math.atan2(self.rot[1], self.rot[0])) % 360.0
	
	def Nudge(self, x: float, y: float):
		"""
		Move this object in a direction (x, y)
		"""

		self.pos[0] += x
		self.pos[1] += y
	
	def NudgeForward(self, distance: float = 1.0):
		"""
		Move object in the direction of its forward rotation by a distance
		"""
		self.pos[0] += self.rot[0] * distance
		self.pos[1] += self.rot[1] * distance
	
	def NudgeBackward(self, distance: float = 1.0):
		"""
		Move object in the direction of its backward rotation by a distance
		"""
		self.NudgeForward(-distance)
	
	def NudgeRight(self, distance: float = 1.0):
		"""
		Move object in the direction of its right-side rotation by a distance
		"""
		self.pos[0] += self.rot[1] * distance
		self.pos[1] += self.rot[0] * distance
	
	def NudgeLeft(self, distance: float = 1.0):
		"""
		Move object in the direction of its left-side rotation by a distance
		"""
		self.NudgeRight(-distance)
	
	def RotateByAngle(self, degree: float):
		"""
		@param degree degrees/tick
		"""
		radian = math.radians(degree % 360)
		vector = [math.cos(radian), math.sin(radian)]
		self.rot = MultiplyVectors(self.rot, vector)
		self.rot = normalizeVector(self.rot)