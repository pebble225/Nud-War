#this could get merged with map manager depending on complexity

from NudWar.game.gameObject import GameObject
from NudWar.game.region import Region
from NudWar.game.nud import Nud

from NudWar.data.dataBase import DataBase
from NudWar.data.unitData import UnitData

from NudWar.manager.nudManager import NudManager
from NudWar.render.window import Window

class RegionManager:
	def __init__(self):
		self.nudManager: NudManager = None
		self.window: Window = None

		self.database: UnitData = None

	def ImportModules(self, nudManager: NudManager, window: Window):
		self.nudManager = nudManager
		self.window = window

	def ImportData(self, database: UnitData):
		self.database = database

	def RealTimeUpdate(self, region: Region):
		for obj in region.objects:
			if isinstance(obj, Nud):
				self.nudManager.Entry(obj, region)

	def CreateBasicNud(self, region: Region, x: float = 0, y: float = 0) -> Nud:
			unitData = self.database.unitData
			nud = Nud(unitData.ToMetersPerTick(10.0), unitData.ToMetersPerTick(180.0))
			nud.SetPosition(x, y)
			region.objects.append(nud)
			return nud

	def AddGameObject(self, region: Region, gameObject: GameObject):
		region.objects.append(gameObject)