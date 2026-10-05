from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action

from NudWar.game.behavior.nud.navigate import Navigate
from NudWar.game.behavior.nud.idle import Idle
from NudWar.game.behavior.nud.wander import Wander

if TYPE_CHECKING:
	from NudWar.game.nud import Nud
	from NudWar.game.map import Map
	from NudWar.game.region import Region


from NudWar.data.dataBase import DataBase
from NudWar.data.unitData import UnitData

from NudWar.utils.rng import LCG

class Nomad(Action):
	WANDER = 0
	TRAVEL = 1
	def __init__(self, database: DataBase, ran: LCG, parentNud: Nud, map: Map, currentRegion: Region, parentAction: Action = None):
		super().__init__(parentNud, parentAction)

		self.counter = Nomad.WANDER
		self.database = database
		self.ran = ran
		self.map = map

	def Update(self, gameTime: int):
		return None

	def Update2(self, gameTime: int, currentRegion: Region): # need to reconsider storing behavior with the actions
		unitData: UnitData = self.database.unitData

		if self.counter == Nomad.WANDER:
			self.counter = Nomad.TRAVEL

			return Idle(gameTime, int(unitData.ToTicks(self.ran.floatRange(30.0, 60.0))), self.parentNud, self, 
				Wander(self.parentNud, self.ran, self.database)
			)
		elif self.counter == Nomad.TRAVEL:
			self.counter = Nomad.WANDER

			regions = self.map.GetAllRegions()
			targetRegion = regions[self.ran.intRange(0, len(regions)-1)]

			return Navigate(currentRegion, targetRegion, self.map, self.parentNud, self.database, self)