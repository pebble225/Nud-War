from NudWar.game.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region
from NudWar.render.window import Window
from NudWar.utils.rng import RNG, LCG

from NudWar.data.unitData import UnitData
from NudWar.data.behaviorData import BehaviorData
from NudWar.data.dataBase import DataBase

from NudWar.game.behavior.nud.action import Action
from NudWar.game.behavior.nud.moveTo import MoveTo
from NudWar.game.behavior.nud.wander import Wander
from NudWar.game.behavior.nud.travelTo import TravelTo
from NudWar.game.behavior.nud.navigate import Navigate

from NudWar.utils.pumpy import *

import math

class NudManager:
	def __init__(self):
		"""
		Possibly depricated manager.
		"""
		self.map: Map = None
		self.camera: Camera = None
		self.window: Window = None
		self.ran: LCG = None

		self.database: DataBase = None
	
	def ImportModules(self,  map: Map, camera: Camera, window: Window, ran: LCG):
		self.map = map
		self.camera = camera
		self.window = window
		self.ran = ran

	def ImportData(self, dataBase: DataBase):
		self.database = dataBase
	
	def Entry(self, nud: Nud | None, currentRegion: Region):
		if nud.action is None:


			nud.AddNewAction(Wander(nud, self.ran, self.database))
			#nud.AddNewAction(Navigate(currentRegion, self.map.GetRegion(1, 1), self.map, nud, self.database, Wander(nud, self.ran, self.database)))

		assert nud.action is not None
		
		nud.action = nud.action.Update(self.window.gameTime)

		