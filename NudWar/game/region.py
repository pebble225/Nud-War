import weakref

from NudWar.game.transformGameObject import TransformGameObject

from NudWar.game.nud import Nud

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

		self.north = None
		self.east = None
		self.south = None
		self.west = None

		self.objects = []

	def WhereIs(self, region: "Region"):# might not be used
		if not self.north is None and self.north() is region:
			return Region.NORTH
		if not self.east is None and self.north() is region:
			return Region.EAST
		if not self.south is None and self.north() is region:
			return Region.SOUTH
		if not self.west is None and self.north() is region:
			return Region.WEST
		return None

	def LinkRegion(self, direction: str, region: "Region"):
		if direction == Region.NORTH:
			self.north = weakref.ref(region)
		elif direction == Region.EAST:
			self.east = weakref.ref(region)
		elif direction == Region.SOUTH:
			self.south = weakref.ref(region)
		elif direction == Region.WEST:
			self.west = weakref.ref(region)