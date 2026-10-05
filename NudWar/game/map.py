from abc import ABC, abstractmethod

from NudWar.game.region import Region
from NudWar.game.gameObject import GameObject

from NudWar.data.mapData import MapData

from NudWar.utils.pumpy import *

class Map(GameObject):
	def __init__(self, mapData: MapData):
		super().__init__()
		self.regions = {}

		self.mapData = mapData

	def GetAllRegions(self) -> list[Region]:
		return list(self.regions.values())
	
	def GetRegion(self, x: int, y: int) -> Region | None:
		if (x, y) in self.regions:
			return self.regions[(x, y)]
		else:
			return None

	def GetUnweightedPath(self, start: Region, end: Region, allRegions: list[Region]):
		if start is end:
			return [start]

		class PathObject(ABC):
			def __init__(self, region: Region, cost: float = None, stepIndex: int = None, pathList: list[Region] = None):
				self.region = region
				self.cost = cost
				self.stepIndex = stepIndex
				self.pathList = pathList

			def ClonePathAndAdd(self, region: Region):
				return [*self.pathList, region]
		
		unsearched: list[PathObject] = []
		searched: list[PathObject] = []
		adjacent: list[PathObject] = []

		# populate the arrays

		startPathObj: PathObject = None
		endPathObj: PathObject = None

		for region in allRegions:
			if region is start:
				startPathObj = PathObject(region, 0, 0, [region])
				searched.append(startPathObj)
			elif region is end:
				endPathObj = PathObject(region)
				unsearched.append(endPathObj)
			else:
				unsearched.append(PathObject(region))

		# set up the starting adjacents

		targetAdjacents: list[Region] = start.GetAdjacents()

		for i, pathObj in reversed(list(enumerate(unsearched))):
			if pathObj.region in targetAdjacents:
				# move to adjacent list
				adjacent.append(pathObj)
				unsearched.pop(i)

				# step index
				pathObj.stepIndex = startPathObj.stepIndex + 1

				# costs
				d = distanceFormula(pathObj.region.GetPosition(), end.GetPosition()) / self.mapData.REGION_SIZE
				pathObj.cost = d * self.mapData.PATHING_DISTANCE_WEIGHT + pathObj.stepIndex * self.mapData.PATHING_STEP_WEIGHT

				# path list
				pathObj.pathList = startPathObj.ClonePathAndAdd(pathObj.region)

				if pathObj.region is end:
					return pathObj.pathList

		# main iteration

		while len(adjacent) > 0:
			# search for the lowest cost

			targetObj: PathObject = adjacent[0]
			lowestCost = targetObj.cost
			for obj in adjacent:
				if obj.cost < lowestCost:
					targetObj = obj
					lowestCost = obj.cost

			# move selected object to searched

			searched.append(targetObj)
			adjacent.remove(targetObj)

			targetAdjacents = targetObj.region.GetAdjacents()

			# find selected object's adjacent regions and generate them

			for i, adjacentObj in reversed(list(enumerate(unsearched))):
				if adjacentObj.region in targetAdjacents:
					if adjacentObj in unsearched:
						adjacent.append(adjacentObj)
						unsearched.pop(i)

						adjacentObj.stepIndex = targetObj.stepIndex + 1

						d = distanceFormula(adjacentObj.region.GetPosition(), end.GetPosition()) / self.mapData.REGION_SIZE
						adjacentObj.cost = d * self.mapData.PATHING_DISTANCE_WEIGHT + adjacentObj.stepIndex * self.mapData.PATHING_STEP_WEIGHT

						adjacentObj.pathList = targetObj.ClonePathAndAdd(adjacentObj.region)

						if adjacentObj.region is end:
							return adjacentObj.pathList

		return None # returns if adjacent list reaches zero before the end region was found, meaning there is no valid path to the desination