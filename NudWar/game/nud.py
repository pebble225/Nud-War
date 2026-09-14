from NudWar.game.transformGameObject import TransformGameObject


class Nud(TransformGameObject):
	def __init__(self, moveSpeed: float, rotationSpeed: float):
		super().__init__()

		self.SetScale(2.0)

		self.moveSpeed = moveSpeed
		self.rotationSpeed = rotationSpeed

	def GetMoveSpeed(self) -> float:
		return self.moveSpeed
	
	def GetRotationSpeed(self) -> float:
		return self.rotationSpeed

	def MoveForward(self, distance: float):
		moveSpeed = self.GetMoveSpeed()
		distance = moveSpeed if distance > moveSpeed else distance
		self.NudgeForward(distance)