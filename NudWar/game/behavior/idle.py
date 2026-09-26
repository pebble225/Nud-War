from typing import TYPE_CHECKING

from NudWar.game.behavior.action import Action
from NudWar.utils.timer import Timer

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Idle(Action):
	def __init__(self, gameTime: int, duration: int, parent: Nud):
		"""
		@param gameTime The current in game time in ticks.
		@param waitTime The amount of time needed to wait in ticks.
		"""
		super().__init__(parent)
		self.parent = parent
		self.timer = Timer(gameTime, duration)

	def Update(self, gameTime: int) -> int:
		if self.timer.IsCompleted(gameTime):
			return Action.COMPLETED
		else:
			return Action.RUNNING