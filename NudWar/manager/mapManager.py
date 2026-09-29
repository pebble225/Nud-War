from NudWar.game.map import Map
from NudWar.game.region import Region
from NudWar.manager.regionManager import RegionManager
from NudWar.game.portal import Portal

from NudWar.data.mapData import MapData

class MapManager:
	def __init__(self):
		self.map: Map = None
		self.regionManager: RegionManager = None

		self.mapData: MapData = None

	def ImportModules(self, map: Map, regionManager: RegionManager):
		self.map = map
		self.regionManager = regionManager

	def ImportData(self, mapData: MapData):
		self.mapData = mapData
	
	def GetAllRegions(self) -> list[Region]:
		return list(self.map.regions.values())
	
	def AddRegion(self, x: int, y: int) -> Region:
		"""
		Adding region to the same coordinate as another should override and discard the old region.
		"""
		region = Region(x, y)
		self.map.regions[(x, y)] = region
		return region
	
	def GetRegion(self, x: int, y: int) -> Region | None:
		if (x, y) in self.map.regions:
			return self.map.regions[(x, y)]
		else:
			return None

	def UpdateAll(self):
		"""
		Updates all of the regions in the map in real time.
		"""

		for region in self.GetAllRegions():
			self.regionManager.RealTimeUpdate(region)

	def LinkHorizontal(self, left: tuple, right: tuple):
		"""
		Logically links two regions together horizontally. Used in portal generation.
		"""
		leftRegion: Region = self.map.regions[left]
		rightRegion: Region = self.map.regions[right]

		leftRegion.LinkRegion(Region.EAST, rightRegion)
		rightRegion.LinkRegion(Region.WEST, leftRegion)

	def LinkVertical(self, top: tuple, bottom: tuple):
		"""
		Logically links two regions together vertically. Used in portal generation.
		"""
		topRegion = self.map.regions[top]
		bottomRegion = self.map.regions[bottom]

		topRegion.LinkRegion(Region.SOUTH, bottomRegion)
		bottomRegion.LinkRegion(Region.NORTH, topRegion)

	def GeneratePortals(self):
		"""
		Generates portals from the region links.
		Please don't run this more than once per map lol.
		"""

		regions = self.GetAllRegions()

		for region in regions:
			if region.south is not None:
				south = region.south()

				portal = Portal()
				portal.SetPosition(self.mapData.REGION_SIZE//2, self.mapData.REGION_SIZE - self.mapData.PORTAL_DISTANCE_TO_EDGE)
				self.regionManager.AddGameObject(region, portal)

				southportal = Portal()
				southportal.SetPosition(self.mapData.REGION_SIZE//2, self.mapData.PORTAL_DISTANCE_TO_EDGE)
				self.regionManager.AddGameObject(south, southportal)

				portal.AddDestination(southportal)
				southportal.AddDestination(portal)

			if region.east is not None:
				east = region.east()

				portal = Portal()
				portal.SetPosition(self.mapData.REGION_SIZE - self.mapData.PORTAL_DISTANCE_TO_EDGE, self.mapData.REGION_SIZE//2)
				self.regionManager.AddGameObject(region, portal)

				eastportal = Portal()
				eastportal.SetPosition(self.mapData.PORTAL_DISTANCE_TO_EDGE, self.mapData.REGION_SIZE//2)
				self.regionManager.AddGameObject(east, eastportal)

				portal.AddDestination(eastportal)
				eastportal.AddDestination(portal)