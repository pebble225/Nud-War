from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from NudWar.game.behavior.nud.action import Action
from NudWar.game.behavior.nud.idle import Idle
from NudWar.game.behavior.nud.moveTo import MoveTo

from NudWar.data.unitData import UnitData
from NudWar.utils.rng import LCG

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Wander(Action):
	def __init__(self, parent: Nud, ran: LCG, unitData: UnitData, parentAction: Action | None = None):
		super().__init__(parent, parentAction)

		self.nextAction = "idle"
		self.ran = ran
		self.unitData = unitData

	def Update(self, gameTime: int) -> "Action":
		if self.nextAction == "idle":
			self.nextAction = "move"

			return Idle(
				gameTime,
				int(self.unitData.ToTicks(self.ran.floatRange(2.0, 8.0))),
				self.parentNud,
				self
			)
		elif self.nextAction == "move":
			self.nextAction = "idle"

			return MoveTo(
				[
					self.ran.intRange(1, 99),
					self.ran.intRange(1, 99)
				],
				self.parentNud,
				self,
				self.unitData.ToMetersPerTick(6) # replace with constant
			)
		else:
			return None