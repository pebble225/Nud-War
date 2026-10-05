from NudWar.data.behaviorData import BehaviorData
from NudWar.data.mapData import MapData
from NudWar.data.renderData import RenderData
from NudWar.data.unitData import UnitData

class DataBase:
	def __init__(self):
		self.unitData = UnitData()
		self.renderData = RenderData(self.unitData)
		self.mapData = MapData()
		self.behaviorData = BehaviorData()