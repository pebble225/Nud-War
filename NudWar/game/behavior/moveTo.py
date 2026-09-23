from typing import TYPE_CHECKING

from NudWar.game.behavior.action import Action
from NudWar.utils.pumpy import *

import numpy as np

if TYPE_CHECKING:
	from NudWar.game.nud import Nud

class MoveTo(Action):
	def __init__(self, pos: tuple[float], parent: Nud):
		"""
		@param pos [x: float, y: float]
		"""

		super().__init__()
		self.parent = parent
		self.pos = pos

	def run(self, gameTime: int):
		speed = self.parent.moveSpeed if (speed is None or (not (speed > 0)) or speed > self.parent.moveSpeed) else speed
	
		angleTolerance = 0.01
		distanceTolerance = 0.01

		distance = distanceFormula(self.parent.pos, self.pos)

		destinationVector = [self.pos[0]-nud.pos[0], self.pos[1]-self.parent.pos[1]]
		destinationVector = normalizeVector(destinationVector)
		turningVector = divideVectors(destinationVector, self.parent.rot)
		angle = np.degrees(np.atan2(turningVector[1], turningVector[0]))

		if np.abs(angle) < angleTolerance:
			if distance < self.parent.moveSpeed:
				if distance < distanceTolerance:
					return Action.FINISHED
				else:
					# distanceTolerance < distance < self.parent.moveSpeed
					self.parent.MoveForward(distance - (distanceTolerance/100))

					# the theory is the nud will stop a one hundreth of the distanceTolerance behind the target
					# and prevent the nud from turning again before completing the action
			else:
				self.parent.MoveForward(speed)
		else:
			self.parent.Turn(angle)

		return Action.RUNNING