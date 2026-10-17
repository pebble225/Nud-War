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
	from NudWar.game.nuds.nud import Nud

class Wander(Action):
	def __init__(self, parentAction: Action | None = None):
		super().__init__(parentAction)

		self.counter = 0