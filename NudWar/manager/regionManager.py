#this could get merged with map manager depending on complexity

from NudWar.game.region import Region
from NudWar.game.nud import Nud
from NudWar.manager.nudManager import NudManager

class RegionManager:
	def __init__(self, nudManager: NudManager):
		self.nudManager = nudManager

	def RealTimeUpdate(self, region: Region):
		for obj in region.objects:
			if isinstance(obj, Nud):
				self.nudManager.Entry(obj, region)