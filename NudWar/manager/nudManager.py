from NudWar.game.nuds.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region
from NudWar.render.window import Window
from NudWar.utils.rng import RNG, LCG

from NudWar.data.unitData import UnitData
from NudWar.data.behaviorData import BehaviorData
from NudWar.data.dataBase import DataBase
from NudWar.data.mapData import MapData

from NudWar.game.behavior.nud.action import Action
from NudWar.game.behavior.nud.moveTo import MoveTo
from NudWar.game.behavior.nud.wander import Wander
from NudWar.game.behavior.nud.navigate import Navigate
from NudWar.game.behavior.nud.nomad import Nomad
from NudWar.game.behavior.nud.idle import Idle

from NudWar.utils.pumpy import *

import warnings
import math

class NudManager:
	def __init__(self):
		"""
		Responsible for executing the actions of nuds.
		"""
		self.map: Map = None
		self.camera: Camera = None
		self.window: Window = None
		self.ran: LCG = None

		self.database: DataBase = None
		self.unitData: UnitData = None
		self.behaviorData: BehaviorData = None
		self.mapData: MapData = None
	
	def ImportModules(self,  map: Map, camera: Camera, window: Window, ran: LCG):
		self.map = map
		self.camera = camera
		self.window = window
		self.ran = ran

	def ImportData(self, database: DataBase):
		self.database = database
		self.unitData = database.unitData
		self.behaviorData = database.behaviorData
		self.mapData = database.mapData

	def Idle(self, region: Region, nud: Nud, idle: Idle):
		if idle.timer.IsCompleted(self.window.gameTime):
			return idle.parentAction
		else:
			if idle.whileIdle is not None:
				idle.whileIdle = self.ActionSwitch(region, nud, idle.whileIdle) # RECURSIVE
			return idle

	def MoveTo(self, nud: Nud, moveTo: MoveTo):
		if moveTo.speed is None:
			moveTo.speed = nud.moveSpeed

		angleTolerance = 0.01
		distanceTolerance = self.behaviorData.PRECISE_DISTANCE_TOLERANCE
		
		distance = distanceFormula(nud.pos, moveTo.pos) # measured in meters

		if distance < distanceTolerance:
			return moveTo.parentAction

		destinationVector = [moveTo.pos[0]-nud.pos[0], moveTo.pos[1]-nud.pos[1]]
		destinationVector = normalizeVector(destinationVector)
		turningVector = divideVectors(destinationVector, nud.rot)
		angle = np.degrees(np.atan2(turningVector[1], turningVector[0]))

		if np.abs(angle) < angleTolerance: # if the nud is facing the target, proceed to movement
			if distance < moveTo.speed:
				nud.MoveForward(distance)
				return moveTo.parentAction
			else:
				if moveTo.speed is None:
					nud.MoveForward(minValue(self.unitData.ToMetersPerTick(self.behaviorData.WANDER_SPEED), moveTo.speed))
				else:
					nud.MoveForward(minValue(self.unitData.ToMetersPerTick(self.behaviorData.WANDER_SPEED), moveTo.speed))
		else:
			nud.Turn(angle)

		return moveTo

	def Navigate(self, region: Region, nud: Nud, navigate: Navigate):
		if navigate.path is None:
			navigate.path = self.map.GetUnweightedPath(region, navigate.destination)
			navigate.travelCounter = 0
		if len(navigate.path) > 1:
			destinationRegion = navigate.path[1]
			match navigate.travelCounter:
				case 0:
					portal = region.WhichWayTo(destinationRegion)
					if nud.IsWithinDistanceTo(portal, self.behaviorData.STANDARD_DISTANCE_TOLERANCE):
						navigate.travelCounter += 1
						return navigate
					else:
						return MoveTo(pos = portal.pos, parentAction = navigate)
				case 1:
					navigate.travelCounter += 1
					return Idle(self.window.gameTime, self.unitData.ToTicks(self.behaviorData.TELEPORT_WAIT_COST), parentAction = navigate)
				case 2:
					navigate.travelCounter = 0
					region.objects.remove(nud)
					destinationRegion.objects.append(nud)
					destinationPortal = destinationRegion.WhichWayTo(region)
					nud.SetPosition2(destinationPortal.pos)
					navigate.path.pop(0)
					return navigate
				case None:
					return None
				case _:
					return None
		else:
			return navigate.parentAction

	def Nomad(self, nomad: Nomad):
		if nomad.counter == Nomad.WANDER:
			nomad.counter = Nomad.TRAVEL
			return Idle(self.window.gameTime, int(self.unitData.ToTicks(self.ran.floatRange(30.0, 60.0))),
			            whileIdle = Wander(), parentAction = nomad)
		elif nomad.counter == Nomad.TRAVEL:
			nomad.counter = Nomad.WANDER

			regions = self.map.GetAllRegions()
			return Navigate(regions[self.ran.intRange(0, len(regions)-1)], nomad)

	def Wander(self, nud: Nud, wander: Wander):
		match wander.counter:
			case 0:
				wander.counter = 1

				return Idle(
					self.window.gameTime,
					int(self.unitData.ToTicks(self.ran.floatRange(2.0, 8.0))),
					parentAction = wander
				)
			case 1:
				wander.counter = 0

				if self.ran.intRange(1, 4) < 4:
					action = MoveTo(
						[
							self.ran.intRange(self.mapData.BORDER_PADDING, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING),
							self.ran.intRange(self.mapData.BORDER_PADDING, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING)
						],
						parentAction = wander
					)
					return action
				else:
					x = self.ran.intRange(
						maxValue(self.mapData.BORDER_PADDING, nud.GetX()-self.behaviorData.WANDER_SMALL_STEP_DISTANCE),
						minValue(nud.GetX()+self.behaviorData.WANDER_SMALL_STEP_DISTANCE, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING)
					)
					y = self.ran.intRange(
						maxValue(self.mapData.BORDER_PADDING, nud.GetY()-self.behaviorData.WANDER_SMALL_STEP_DISTANCE),
						minValue(nud.GetY()+self.behaviorData.WANDER_SMALL_STEP_DISTANCE, self.mapData.REGION_SIZE - self.mapData.BORDER_PADDING)
					)

					action = MoveTo(
						[x, y],
						parentAction = wander
					)
					return action
			case _:
				return None
	
	###################################################
	
	def ActionSwitch(self, region: Region, nud: Nud, action: Action) -> Action:
		match action: # should be sorted from most called to least called
			case Idle():
				return self.Idle(region, nud, action)
			case MoveTo():
				return self.MoveTo(nud, action)
			case Navigate():
				return self.Navigate(region, nud, action)
			case Wander():
				return self.Wander(nud, action)
			case Nomad():
				return self.Nomad(action)
			case None:
				return None
			case _:
				raise ValueError("Could not switch to nud action!")

	def Entry(self, region: Region, nud: Nud):
		if nud.action is None:
			nud.action = Nomad()

		nud.action = self.ActionSwitch(region, nud, nud.action)