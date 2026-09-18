from NudWar.game.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region
from NudWar.render.window import Window

from NudWar.utils.pumpy import *

import math

class NudManager:
	def __init__(self, map: Map, camera: Camera, window: Window):
		self.map = map
		self.camera = camera
		self.window = window
	
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

	def MoveToPosition(self, nud: Nud, pos: tuple[float], speed: float = 999999):
		"""
		@param pos Relative to position of the current region
		"""

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
				self.MaxForward(nud)
		else:
			self.Turn(nud, angle)
		
	
	# entry
	
	def Entry(self, nud: Nud, currentRegion: Region):
		self.MoveToPosition(nud, (50, 50))