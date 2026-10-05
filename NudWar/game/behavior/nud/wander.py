from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from NudWar.game.behavior.nud.action import Action
from NudWar.game.behavior.nud.idle import Idle
from NudWar.game.behavior.nud.moveTo import MoveTo

from NudWar.data.dataBase import DataBase
from NudWar.data.unitData import UnitData
from NudWar.data.mapData import MapData
from NudWar.data.behaviorData import BehaviorData

from NudWar.utils.rng import LCG
from NudWar.utils.pumpy import *

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class Wander(Action):
	def __init__(self, parent: Nud, ran: LCG, database: DataBase, parentAction: Action | None = None):
		super().__init__(parent, parentAction)

		self.nextAction = "idle"
		self.ran = ran
		self.unitData = database.unitData
		self.behaviorData = database.behaviorData
		self.mapData = database.mapData

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

			if self.ran.intRange(1, 3) < 3:
				return MoveTo(
					[
						self.ran.intRange(self.mapData.BORDER_PADDING, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING),
						self.ran.intRange(self.mapData.BORDER_PADDING, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING)
					],
					self.parentNud,
					self,
					self.unitData.ToMetersPerTick(6) # replace with constant
				)
			else:
				x = self.ran.intRange(
					maxValue(self.mapData.BORDER_PADDING, self.parentNud.GetX()-self.behaviorData.WANDER_SMALL_STEP_DISTANCE),
					minValue(self.parentNud.GetX()+self.behaviorData.WANDER_SMALL_STEP_DISTANCE, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING)
				)
				y = self.ran.intRange(
					maxValue(self.mapData.BORDER_PADDING, self.parentNud.GetY()-self.behaviorData.WANDER_SMALL_STEP_DISTANCE),
					minValue(self.parentNud.GetY()+self.behaviorData.WANDER_SMALL_STEP_DISTANCE, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING)
				)

				return MoveTo(
					[x, y],
					self.parentNud,
					self,
					self.unitData.ToMetersPerTick(6) # replace with constant
				)
		else:
			return None