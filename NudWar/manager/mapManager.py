from NudWar.game.map import Map
from NudWar.game.region import Region
from NudWar.manager.regionManager import RegionManager
from NudWar.game.portal import Portal

from NudWar.data.dataBase import DataBase
from NudWar.data.mapData import MapData

class MapManager:
	def __init__(self):
		self.map: Map = None
		self.regionManager: RegionManager = None

		self.database: DataBase = None

	def ImportModules(self, map: Map, regionManager: RegionManager):
		self.map = map
		self.regionManager = regionManager

	def ImportData(self, database: DataBase):
		self.database = database
	
	def GetAllRegions(self) -> list[Region]:
		return self.map.GetAllRegions()
	
	def AddRegion(self, x: int, y: int) -> Region:
		"""
		Adding region to the same coordinate as another should override and discard the old region.
		"""
		region = Region(x, y)
		self.map.regions[(x, y)] = region
		return region
	
	def GetRegion(self, x: int, y: int) -> Region | None:
		return self.map.GetRegion(x, y)

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

		mapData = self.database.mapData
		REGION_SIZE = mapData.REGION_SIZE
		PORTAL_DISTANCE_TO_EDGE = mapData.PORTAL_DISTANCE_TO_EDGE


		regions = self.GetAllRegions()

		for region in regions:
			if region.south is not None:
				south: Region = region.south

				portal = Portal()
				region.southPortal = portal
				portal.SetPosition(REGION_SIZE//2, REGION_SIZE - PORTAL_DISTANCE_TO_EDGE)
				self.regionManager.AddGameObject(region, portal)

				southRegionPortal = Portal()
				south.northPortal = southRegionPortal
				southRegionPortal.SetPosition(REGION_SIZE//2, PORTAL_DISTANCE_TO_EDGE)
				self.regionManager.AddGameObject(south, southRegionPortal)

				portal.AddDestination(southRegionPortal)
				southRegionPortal.AddDestination(portal)

			if region.east is not None:
				east: Region = region.east

				portal = Portal()
				region.eastPortal = portal
				portal.SetPosition(REGION_SIZE - PORTAL_DISTANCE_TO_EDGE, REGION_SIZE//2)
				self.regionManager.AddGameObject(region, portal)

				eastRegionPortal = Portal()
				east.westPortal = eastRegionPortal
				eastRegionPortal.SetPosition(PORTAL_DISTANCE_TO_EDGE, REGION_SIZE//2)
				self.regionManager.AddGameObject(east, eastRegionPortal)

				portal.AddDestination(eastRegionPortal)
				eastRegionPortal.AddDestination(portal)