from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action
from NudWar.utils.timer import Timer

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Idle(Action):
	def __init__(self, gameTime: int, duration: int, parentNud: Nud, parentAction: Action, whileIdle: Action | None = None):
		"""
		@param gameTime The current in game time in ticks.
		@param duration The amount of time needed to wait in ticks.
		"""
		super().__init__(parentNud, parentAction)
		self.parentNud = parentNud
		self.timer = Timer(gameTime, duration)

		self.whileIdle = whileIdle

	def Update(self, gameTime: int) -> int:
		if self.timer.IsCompleted(gameTime):
			return self.parentAction
		else:
			if self.whileIdle is not None:
				self.whileIdle.Update(gameTime)
			return self