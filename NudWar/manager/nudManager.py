from NudWar.game.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region
from NudWar.render.window import Window
from NudWar.utils.rng import RNG, LCG
from NudWar.data.unitData import UnitData

from NudWar.game.behavior.action import Action
from NudWar.game.behavior.nud.moveTo import MoveTo
from NudWar.game.behavior.nud.wander import Wander

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

		self.unitData: UnitData = None
	
	def ImportModules(self,  map: Map, camera: Camera, window: Window, ran: LCG):
		self.map = map
		self.camera = camera
		self.window = window
		self.ran = ran

	def ImportData(self, unitData: UnitData):
		self.unitData = unitData
	
	def Entry(self, nud: Nud, currentRegion: Region):
		if len(nud.actionQueue) < 1:
			nud.AddNewAction(Wander(nud, self.ran, self.unitData))
		action: Action = nud.actionQueue[-1]
		if action.Update(self.window.gameTime) == Action.COMPLETED:
			nud.RemoveLastAction()