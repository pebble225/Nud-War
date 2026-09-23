from NudWar.game.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region
from NudWar.render.window import Window
from NudWar.utils.rng import RNG, LCG

from NudWar.game.behavior.action import Action
from NudWar.game.behavior.moveTo import MoveTo
from NudWar.game.behavior.wander import Wander

from NudWar.utils.pumpy import *

import math

class NudManager:
	def __init__(self, map: Map, camera: Camera, window: Window, ran: LCG):
		self.map = map
		self.camera = camera
		self.window = window
		self.ran = ran
	
	# Layer 1

	def MoveForward(self, nud: Nud, distance: float):
		moveSpeed = nud.GetMoveSpeed()
		distance = moveSpeed if distance > moveSpeed else distance
		nud.NudgeForward(distance)

	def MaxForward(self, nud: Nud):
		nud.NudgeForward(nud.GetMoveSpeed())
	
	def TurnRight(self, nud: Nud, amount: float):
		rotationSpeed = nud.GetRotationSpeed()
		amount = rotationSpeed if amount > rotationSpeed else amount
		nud.RotateByAngle(amount)
	
	def TurnLeft(self, nud: Nud, amount: float):
		rotationSpeed = nud.GetRotationSpeed()
		amount = rotationSpeed if amount > rotationSpeed else amount
		nud.RotateByAngle(-amount)

	def Turn(self, nud: Nud, amount: float):
		rotationSpeed = nud.GetRotationSpeed()

		if amount < -rotationSpeed:
			amount = -rotationSpeed
		elif amount > rotationSpeed:
			amount = rotationSpeed

		nud.RotateByAngle(amount)
	
	def TurnRightMax(self, nud: Nud):
		nud.RotateByAngle(nud.rotationSpeed)
	
	def TurnLeftMax(self, nud: Nud):
		nud.RotateByAngle(-nud.rotationSpeed)

	# Layer 2

	def MoveToPosition(self, nud: Nud, pos: tuple[float], speed: float | None = None):
		"""
		@param pos Relative to position of the current region
		@param speed Measured in units per tick
		"""

		speed = nud.moveSpeed if (speed is None or (not (speed > 0)) or speed > nud.moveSpeed) else speed

		angleTolerance = 0.01
		distanceTolerance = 0.01

		distance = distanceFormula(nud.pos, pos)

		destinationVector = [pos[0]-nud.pos[0], pos[1]-nud.pos[1]]
		destinationVector = normalizeVector(destinationVector)
		turningVector = divideVectors(destinationVector, nud.rot)
		angle = np.degrees(np.atan2(turningVector[1], turningVector[0]))

		if np.abs(angle) < angleTolerance:
			if distance < nud.moveSpeed:
				if distance < distanceTolerance:
					return # completed condition
				else:
					# distanceTolerance < distance < nud.moveSpeed
					self.MoveForward(nud, distance - (distanceTolerance/100))

					# the theory is the nud will stop a one hundreth of the distanceTolerance behind the target
					# and prevent the nud from turning again before completing the action
			else:
				self.MoveForward(nud, speed)
		else:
			self.Turn(nud, angle)

	# Layer 3

	def Wander(self, nud: Nud):
		pass
		
	
	# entry
	
	def Entry(self, nud: Nud, currentRegion: Region):
		if len(nud.actionQueue) < 1:
			nud.AddNewAction(Wander(nud))
		action: Action = nud.actionQueue[-1]
		if action.Update(self.window.gameTime) == Action.COMPLETED:
			nud.RemoveLastAction()