from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action
from NudWar.game.behavior.nud.travelTo import TravelTo

from NudWar.data.dataBase import DataBase

if TYPE_CHECKING:
	from NudWar.game.nud import Nud
	from NudWar.game.map import Map
	from NudWar.game.region import Region

class Navigate(Action):
	def __init__(self, startRegion: Region, endRegion: Region, map: Map, parentNud: Nud, database: DataBase, parentAction = None):
		super().__init__(parentNud, parentAction)

		self.path: list[Region] | None = map.GetUnweightedPath(startRegion, endRegion, map.GetAllRegions())
		self.endRegion = endRegion
		self.map = map
		self.database = database

	def Update(self, gameTime: int):
		if self.path is None:
			return None
		if len(self.path) > 1:
			action: Action = TravelTo(self.parentNud, self.path[0], self.path[1], self.database, self)
			self.path.pop(0)
			return action
		else:
			return self.parentAction