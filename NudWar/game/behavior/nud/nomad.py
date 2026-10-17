from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action

from NudWar.game.behavior.nud.navigate import Navigate
from NudWar.game.behavior.nud.idle import Idle
from NudWar.game.behavior.nud.wander import Wander

if TYPE_CHECKING:
	from NudWar.game.nuds.nud import Nud
	from NudWar.game.map import Map
	from NudWar.game.region import Region


from NudWar.data.dataBase import DataBase
from NudWar.data.unitData import UnitData

from NudWar.utils.rng import LCG

class Nomad(Action):
	WANDER = 0
	TRAVEL = 1
	def __init__(self, parentAction: Action = None):
		super().__init__(parentAction)

		self.counter = Nomad.WANDER