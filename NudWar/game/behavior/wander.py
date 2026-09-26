from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from NudWar.game.behavior.action import Action
from NudWar.game.behavior.idle import Idle
from NudWar.game.behavior.moveTo import MoveTo

from NudWar.game.constants import Constants
from NudWar.utils.rng import LCG

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Wander(Action):
	def __init__(self, parent: Nud, ran: LCG):
		super().__init__(parent)

		self.parent = parent
		self.nextAction = "idle"
		self.ran = ran
		self.constants = Constants()

	def Update(self, gameTime: int) -> int:
		if self.nextAction == "idle":
			self.parent.AddNewAction(
				Idle(
					gameTime,
					int(self.constants.ToTicks(
						self.ran.floatRange(2.0, 8.0) # replace both with constant
					)),
					self.parent
				)
			)
			self.nextAction = "move"

			return Action.RUNNING
		elif self.nextAction == "move":
			self.parent.AddNewAction(
				MoveTo(  
					[
						self.ran.intRange(1, 99),
						self.ran.intRange(1, 99)
					],
					self.parent,
					self.constants.ToMetersPerTick(6) # replace with constant
				)
			)
			self.nextAction = "idle"

			return Action.RUNNING
		else:
			return Action.FAILED