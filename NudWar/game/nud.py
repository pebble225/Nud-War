from NudWar.game.transformGameObject import TransformGameObject

from NudWar.game.behavior.action import Action
from NudWar.game.behavior.moveTo import MoveTo

class Nud(TransformGameObject):
	def __init__(self, moveSpeed: float, rotationSpeed: float):
		"""
		@param moveSpeed Measured in units per tick
		@param rotationSpeed Measured in rotations per tick
		"""
		super().__init__()

		self.SetScale(2.0)

		self.actionQueue = []

		# moveSpeed is measured in units per tick
		# rotationSpeed is measured in degrees per tick

		self.moveSpeed = moveSpeed
		self.rotationSpeed = rotationSpeed

	def AddNewAction(self, action: Action):
		self.actionQueue.append(action)

	def RemoveLastAction(self):
		# One of the flaws with the ai setup is that each completed action will generate garbage for the gc
		# If it helps with speed, the gc could be informed after each update to free the memory from completed tasks
		# so that it doesn't build up.
		self.actionQueue.pop()

	# Layer 1
	
	def MoveForward(self, distance: float):
		moveSpeed = self.GetMoveSpeed()
		distance = moveSpeed if distance > moveSpeed else distance
		self.NudgeForward(distance)

	def MaxForward(self):
		self.NudgeForward(self.GetMoveSpeed())
	
	def TurnRight(self, amount: float):
		rotationSpeed = self.GetRotationSpeed()
		amount = rotationSpeed if amount > rotationSpeed else amount
		self.RotateByAngle(amount)
	
	def TurnLeft(self, amount: float):
		rotationSpeed = self.GetRotationSpeed()
		amount = rotationSpeed if amount > rotationSpeed else amount
		self.RotateByAngle(-amount)

	def Turn(self, amount: float):
		rotationSpeed = self.GetRotationSpeed()

		if amount < -rotationSpeed:
			amount = -rotationSpeed
		elif amount > rotationSpeed:
			amount = rotationSpeed

		self.RotateByAngle(amount)
	
	def TurnRightMax(self):
		self.RotateByAngle(self.rotationSpeed)
	
	def TurnLeftMax(self):
		self.RotateByAngle(-self.rotationSpeed)

	def GetMoveSpeed(self) -> float:
		return self.moveSpeed
	
	def GetRotationSpeed(self) -> float:
		return self.rotationSpeed