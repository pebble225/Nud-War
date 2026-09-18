from NudWar.game.gameObject import GameObject
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
	
	def SetPosition(self, x: float, y: float):
		self.pos[0] = x
		self.pos[1] = y
	
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


	def GetRotationAngle(self) -> float:
		return math.degrees(math.atan2(self.rot[1], self.rot[0])) % 360.0
	
	def ToGameSpace(self, vertex: list[float]) -> list[float]:
		"""
		Returns a transformed vertex in game space according to the transform of the game object

		this does not include the camera

		maybe this should be put in renderer
		"""
		outputVertex = [vertex[0], vertex[1]]

		outputVertex = self._MultiplyVectors(vertex, self.rot)
		outputVertex[0] *= self.scale[0]
		outputVertex[1] *= self.scale[1]
		outputVertex[0] += self.pos[0]
		outputVertex[1] += self.pos[1]

		return outputVertex
	
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

	def _NormalizeRotation(self):
		d = math.sqrt(self.rot[0]*self.rot[0]+self.rot[1]*self.rot[1])

		self.rot = [self.rot[0] / d, self.rot[1] / d]
	
	def _NormalizeVector(self, vec: list[float]):
		d = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
		return [vec[0] / d, vec[1] / d]

	def _MultiplyVectors(self, vecA: list[float], vecB: list[float]):
		return [vecA[0]*vecB[0] - vecA[1]*vecB[1], vecA[0]*vecB[1] + vecA[1]*vecB[0]]
	
	def _MultiplyRotationByVector(self, vec: tuple[float]):
		rotation = self._MultiplyVectors(self.rot, vec)
		self.rot[0] = rotation[0]
		self.rot[1] = rotation[1]
	
	def RotateByAngle(self, degree: float):
		radian = math.radians(degree % 360)
		vector = [math.cos(radian), math.sin(radian)]
		self._MultiplyRotationByVector(vector)
		self._NormalizeRotation()