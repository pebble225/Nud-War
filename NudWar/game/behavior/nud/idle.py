from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action
from NudWar.utils.timer import Timer

if TYPE_CHECKING:
	from NudWar.game.nuds.nud import Nud

class Idle(Action):
	def __init__(self, gameTime: int, duration: int, whileIdle: Action | None = None, parentAction: Action | None = None):
		"""
		@param gameTime The current in game time in ticks.
		@param duration The amount of time needed to wait in ticks.
		"""
		super().__init__(parentAction)
		self.timer = Timer(gameTime, duration)

		self.whileIdle = whileIdle