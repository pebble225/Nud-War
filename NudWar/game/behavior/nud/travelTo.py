from typing import TYPE_CHECKING

import warnings

from NudWar.game.behavior.nud.action import Action
from NudWar.game.behavior.nud.moveTo import MoveTo
from NudWar.game.behavior.nud.idle import Idle

from NudWar.data.unitData import UnitData
from NudWar.data.behaviorData import BehaviorData
from NudWar.data.dataBase import DataBase

if TYPE_CHECKING:
	from NudWar.game.nud import Nud
	from NudWar.game.portal import Portal
	from NudWar.game.region import Region

class TravelTo(Action):
	UNVALIDATED = 0
	MOVETO = 1
	WAIT = 2
	TELEPORT = 3
	EXIT_PORTAL = 4

	def __init__(self, parentNud: Nud, departureRegion: Region, destinationRegion: Region, dataBase: UnitData, parentAction: Action = None):
		"""
		@param departureRegion The region the nud is departing from.
		@param destinationRegion The destination the nud will hand itself over to during the transfer.
		"""
		super().__init__(parentNud, parentAction)

		self.departurePortal = departureRegion.WhichWayTo(destinationRegion)
		self.destinationPortal = destinationRegion.WhichWayTo(departureRegion)
		self.departureRegion = departureRegion
		self.destinationRegion = destinationRegion

		self.behaviorData: BehaviorData = dataBase.behaviorData
		self.unitData: UnitData = dataBase.unitData

		self.counter = TravelTo.UNVALIDATED

	def _Validate(self) -> bool:
		if not self.parentNud in self.departureRegion.objects:
			warnings.warn(f"A nud was assigned a travelTo command without being in the departure region.", UserWarning)
			return False
		if not self.departurePortal in self.departureRegion.objects:
			warnings.warn(f"A nud was assigned a travelTo command, but the departure portal is not in the same region.", UserWarning)
			return False
		if not self.destinationPortal in self.destinationRegion.objects:
			warnings.warn(f"A nud was assigned a travelTo command, but the destination portal is in a different region than the desination region.", UserWarning)
			return False
		if self.departurePortal.destination is not self.destinationPortal:
			warnings.warn(f"A nud was assigned a travelTo command where the portals do not connected to one another.", UserWarning)
			return False
		return True

	def Update(self, gameTime: int) -> Action:
		if self.counter == TravelTo.UNVALIDATED:
			if not self._Validate():
				return None
			self.counter = TravelTo.MOVETO
			return self
		elif self.counter == TravelTo.MOVETO:
			if self.parentNud.IsWithinDistanceTo(self.departurePortal, self.behaviorData.STANDARD_DISTANCE_TOLERANCE):
				self.counter = TravelTo.WAIT
				return self
			else:
				return MoveTo(self.departurePortal.pos, self.parentNud, self)
		elif self.counter == TravelTo.WAIT:
			self.counter = TravelTo.TELEPORT
			return Idle(gameTime, self.unitData.ToTicks(self.behaviorData.TELEPORT_WAIT_COST), self.parentNud, self)
		elif self.counter == TravelTo.TELEPORT:
			self.departureRegion.objects.remove(self.parentNud)
			self.destinationRegion.objects.append(self.parentNud)
			self.parentNud.SetPosition2(self.destinationPortal.pos)
			self.counter = TravelTo.EXIT_PORTAL
			return self.parentAction
		elif self.counter == TravelTo.EXIT_PORTAL:
			pass # nuds can move forward according to the way they came in which depends on the direction they came from