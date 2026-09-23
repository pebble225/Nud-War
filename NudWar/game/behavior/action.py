from NudWar.game.gameObject import GameObject
from abc import ABC, abstractmethod

class Action(GameObject):
	FAILED = 0
	COMPLETED = 1
	RUNNING = 2

	def __init__(self):
		super().__init__()

	@abstractmethod
	def Update(self, gameTime: int) -> int:
		raise NotImplementedError

	@abstractmethod
	def checkFlags(self):
		raise NotImplementedError