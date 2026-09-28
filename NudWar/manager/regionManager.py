#this could get merged with map manager depending on complexity

from NudWar.game.region import Region
from NudWar.game.nud import Nud
from NudWar.data.unitData import UnitData

from NudWar.manager.nudManager import NudManager
from NudWar.render.window import Window

class RegionManager:
	def __init__(self):
		self.nudManager: NudManager = None
		self.window: Window = None

		self.unitData: UnitData = None

	def ImportModules(self, nudManager: NudManager, window: Window):
		self.nudManager = nudManager
		self.window = window

	def ImportData(self, unitData: UnitData):
		self.unitData = unitData

	def RealTimeUpdate(self, region: Region):
		for obj in region.objects:
			if isinstance(obj, Nud):
				self.nudManager.Entry(obj, region)

	def CreateBasicNud(self, region: Region, x: float = 0, y: float = 0) -> Nud:
			nud = Nud(self.unitData.ToMetersPerTick(10.0), self.unitData.ToMetersPerTick(180.0))
			nud.SetPosition(x + region.index[0]*Region.SIZE, y + region.index[1]*Region.SIZE)
			region.objects.append(nud)
			return nud