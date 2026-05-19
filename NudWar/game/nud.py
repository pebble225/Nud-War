from abc import ABC, abstractmethod

from NudWar.game.transformGameObject import TransformGameObject


class Nud(TransformGameObject):
	def __init__(self):
		super().__init__()
	
	@abstractmethod
	def Render(self):
		# this is a parent render for debug purposes

		vertices = [
			[-1.0, -0.5],
			[1.0, 0.0],
			[-1.0, 0.5]
		]

		for vertex in vertices:
			vertex[0]

	def MoveForward(self):
		pass

	def MoveLeft(self):
		pass

	def MoveRight(self):
		pass

	def FirePrimaryWeapon(self):
		pass