from NudWar.game.transformGameObject import TransformGameObject


class Nud(TransformGameObject):
	

	def __init__(self):
		super().__init__()

		self.SetScale(2.0)

		self.moveSpeed = 1
		self.rotationSpeed = 10

	def MoveForward(self):
		self.NudgeForward(self.moveSpeed)

	def MoveLeft(self):
		self.RotateByAngle(-self.rotationSpeed)

	def MoveRight(self):
		self.RotateByAngle(self.rotationSpeed)