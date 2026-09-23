from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

from NudWar.game.behavior.action import Action

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Wander(Action):
	def __init__(self, parent: Nud):
		super().__init__()

		self.parent = parent

	def Update(self, gameTime: int) -> int:
		self.parent.TurnRight(90.0 / 60.0)

		return Action.RUNNING