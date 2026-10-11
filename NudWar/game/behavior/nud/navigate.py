from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action

from NudWar.data.dataBase import DataBase

if TYPE_CHECKING:
	from NudWar.game.nud import Nud
	from NudWar.game.map import Map
	from NudWar.game.region import Region

class Navigate(Action):
	def __init__(self, destination: Region, parentAction = None):
		super().__init__(parentAction)

		self.path: list[Region] | None = None
		self.destination = destination # grrrr

		self.travelCounter: int | None = None