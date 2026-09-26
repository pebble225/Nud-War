from typing import TYPE_CHECKING

from NudWar.game.behavior.action import Action
from NudWar.utils.pumpy import *

import numpy as np

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class MoveTo(Action):
	def __init__(self, pos: tuple[float, float], parent: Nud, speed: float | None = None):
		"""
		@param pos [x: float, y: float]
		@param speed Measured in meters/tick.
		"""

		super().__init__(parent)
		self.pos = pos

		if speed is None or speed > parent.moveSpeed or (not (speed > 0)):
			self.speed = parent.moveSpeed
		else:
			self.speed = speed

	def Update(self, gameTime: int):
		angleTolerance = 0.01

		distance = distanceFormula(self.parent.pos, self.pos) # measured in meters

		destinationVector = [self.pos[0]-self.parent.pos[0], self.pos[1]-self.parent.pos[1]]
		destinationVector = normalizeVector(destinationVector)
		turningVector = divideVectors(destinationVector, self.parent.rot)
		angle = np.degrees(np.atan2(turningVector[1], turningVector[0]))

		if np.abs(angle) < angleTolerance: # if the nud is facing the target, proceed to movement
			if distance < self.speed:
				self.parent.MoveForward(distance)
				return Action.COMPLETED
			else:
				self.parent.MoveForward(self.speed)
		else:
			self.parent.Turn(angle)

		return Action.RUNNING