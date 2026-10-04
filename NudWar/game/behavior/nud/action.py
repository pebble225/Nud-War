from typing import TYPE_CHECKING

from NudWar.game.gameObject import GameObject
from abc import ABC, abstractmethod

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Action(GameObject):
	def __init__(self, parentNud: Nud, parentAction: "Action" | None = None):
		super().__init__()
		self.parentNud = parentNud
		self.parentAction = parentAction

	@abstractmethod
	def Update(self, gameTime: int) -> "Action":
		raise NotImplementedError