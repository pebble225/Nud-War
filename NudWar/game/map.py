from NudWar.game.region import Region

class Map:
	def __init__(self):
		self.regions = {}
	
	def GetAllRegions(self) -> list:
		return list(self.regions.values())
	
	def AddRegion(self, x: int, y: int):
		"""
		Adding region to the same coordinate as another should override and discard the old region.
		"""

		self.regions[(x, y)] = Region(x, y)