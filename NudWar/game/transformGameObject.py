from NudWar.game.gameObject import GameObject
import math

class TransformGameObject(GameObject):
	def __init__(self):
		super().__init__()

		self.pos = [0.0, 0.0]
		self.rot = [1.0, 0.0]
		self.scale = [1.0, 1.0]
		self.collisionBoxDim = [1.0, 1.0]
		self.renderObject = None
	
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
	
	def _MultiplyRotationByVector(self, vec: tuple[float]):
		self.rot = [self.rot[0]*vec[0] - self.rot[1]*vec[1], self.rot[0]*vec[1]+self.rot[1]*vec[0]]
	
	def RotateByAngle(self, degree: float):
		radian = (degree % 360.0) * math.pi / 180
		vector = [math.cos(radian), math.sin(radian)]
		self._MultiplyRotationByVector(vector)
		self._NormalizeRotation()