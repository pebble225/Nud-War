from typing import TYPE_CHECKING

from NudWar.game.gameObject import GameObject
from abc import ABC, abstractmethod

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Action(GameObject):
	def __init__(self, parentAction: "Action" | None = None):
		super().__init__()
		self.parentAction = parentAction

	def Deallocate(self):
		"""
		Oh don't mind me. I'm just hanging out in case I'm needed at some point.
		"""
		if self.parentAction is not None:
			self.parentAction.Deallocate()
		self.parentAction = None