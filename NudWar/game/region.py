import weakref

from NudWar.game.transformGameObject import TransformGameObject

from NudWar.game.nud import Nud
from NudWar.game.portal import Portal

class Region(TransformGameObject):
	SIZE = 100 # depricated

	NORTH = "north"
	EAST = "east"
	SOUTH = "south"
	WEST = "west"

	def __init__(self, x: float, y: float):
		super().__init__()

		self.SetPosition(x*Region.SIZE, y*Region.SIZE)
		self.index = [int(x), int(y)]
		self.SetScale(Region.SIZE)

		self.north: Region | None = None
		self.east: Region | None = None
		self.south: Region | None = None
		self.west: Region | None = None

		self.northPortal: Portal | None = None
		self.eastPortal: Portal | None = None
		self.southPortal: Portal | None = None
		self.westPortal: Portal | None = None

		self.objects = []

	def WhereIs(self, region: "Region"):# might not be used
		"""
		Returns the direction a region is from the current region.
		Only works with adjacents.
		"""
		if not self.north is None and self.north is region:
			return Region.NORTH
		if not self.east is None and self.east is region:
			return Region.EAST
		if not self.south is None and self.south is region:
			return Region.SOUTH
		if not self.west is None and self.west is region:
			return Region.WEST
		return None

	def WhichWayTo(self, region: Region) -> Portal | None:
		direction = self.WhereIs(region)

		if direction == Region.NORTH:
			return self.northPortal
		if direction == Region.EAST:
			return self.eastPortal
		if direction == Region.SOUTH:
			return self.southPortal
		if direction == Region.WEST:
			return self.westPortal
		return None

	def IsHorizontalTo(self, region: Region):
			return self.east is region or self.west is region
	
	def IsVerticalTo(self, region: Region):
			return self.north is region or self.south is region	

	def HasNorth(self) -> bool:
		return self.north is not None
	
	def HasEast(self) -> bool:
		return self.east is not None
	
	def HasSouth(self) -> bool:
		return self.south is not None
	
	def HasWest(self) -> bool:
		return self.west is not None

	def GetAdjacents(self):
		"""
		Returns a list of all of the adjacent regions. 
		"""
		arr = []
		if self.north is not None:
			arr.append(self.north)
		if self.east is not None:
			arr.append(self.east)
		if self.south is not None:
			arr.append(self.south)
		if self.west is not None:
			arr.append(self.west)

		return arr

	def LinkRegion(self, direction: str, region: "Region"):
		if direction == Region.NORTH:
			self.north = region
		elif direction == Region.EAST:
			self.east = region
		elif direction == Region.SOUTH:
			self.south = region
		elif direction == Region.WEST:
			self.west = region