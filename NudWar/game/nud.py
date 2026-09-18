from NudWar.game.transformGameObject import TransformGameObject


class Nud(TransformGameObject):
	def __init__(self, moveSpeed: float, rotationSpeed: float):
		"""
		@param moveSpeed Measured in units per tick
		@param rotationSpeed Measured in rotations per tick
		"""
		super().__init__()

		self.SetScale(2.0)

		# moveSpeed is measured in units per tick
		# rotationSpeed is measured in degrees per tick

		self.moveSpeed = moveSpeed
		self.rotationSpeed = rotationSpeed

	def GetMoveSpeed(self) -> float:
		return self.moveSpeed
	
	def GetRotationSpeed(self) -> float:
		return self.rotationSpeed