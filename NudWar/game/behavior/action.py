from typing import TYPE_CHECKING

from NudWar.game.gameObject import GameObject
from abc import ABC, abstractmethod

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Action(GameObject):
	FAILED = 0
	COMPLETED = 1
	RUNNING = 2

	def __init__(self, parent: Nud):
		super().__init__()
		self.parent = parent

	@abstractmethod
	def Update(self, gameTime: int) -> int:
		raise NotImplementedError

	@abstractmethod
	def checkFlags(self):
		raise NotImplementedError