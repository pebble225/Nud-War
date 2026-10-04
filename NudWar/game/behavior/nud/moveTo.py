from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action
from NudWar.utils.pumpy import *

import numpy as np

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class MoveTo(Action):
	def __init__(self, pos: tuple[float, float], parentNud: Nud, parentAction: Action, speed: float | None = None):
		"""
		@param pos [x: float, y: float]
		@param speed Measured in meters/tick.
		"""

		super().__init__(parentNud, parentAction)
		self.pos = pos

		if speed is None or speed > parentNud.moveSpeed or (not (speed > 0)):
			self.speed = parentNud.moveSpeed
		else:
			self.speed = speed

	def Check(self, gameTime: int):
		pass

	def Update(self, gameTime: int):
		angleTolerance = 0.01

		distance = distanceFormula(self.parentNud.pos, self.pos) # measured in meters

		destinationVector = [self.pos[0]-self.parentNud.pos[0], self.pos[1]-self.parentNud.pos[1]]
		destinationVector = normalizeVector(destinationVector)
		turningVector = divideVectors(destinationVector, self.parentNud.rot)
		angle = np.degrees(np.atan2(turningVector[1], turningVector[0]))

		if np.abs(angle) < angleTolerance: # if the nud is facing the target, proceed to movement
			if distance < self.speed:
				self.parentNud.MoveForward(distance)
				return self.parentAction
			else:
				self.parentNud.MoveForward(self.speed)
		else:
			self.parentNud.Turn(angle)

		return self