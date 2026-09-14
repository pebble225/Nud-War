from NudWar.game.map import Map
from NudWar.manager.regionManager import RegionManager

class MapManager:
	def __init__(self, map: Map, regionManager: RegionManager):
		self.map = map
		self.regionManager = regionManager

	def UpdateAll(self):
		"""
		Updates all of the regions in the map in real time. Very slow and cringe.
		"""

		for region in self.map.GetAllRegions():
			self.regionManager.RealTimeUpdate(region)