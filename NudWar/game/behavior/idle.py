from typing import TYPE_CHECKING

from NudWar.game.behavior.action import Action

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Idle:
	def __init__(self, gameTime: int, waitTime: int, parent: Nud):
		"""
		@param gameTime The current in game time in ticks.
		@param waitTime The amount of time needed to wait in ticks.
		"""
		self.parent = parent

	def Update(self, gameTime: int) -> int:
		pass