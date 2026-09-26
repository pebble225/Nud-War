from NudWar.game.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region
from NudWar.render.window import Window
from NudWar.utils.rng import RNG, LCG
from NudWar.game.constants import Constants

from NudWar.game.behavior.action import Action
from NudWar.game.behavior.moveTo import MoveTo
from NudWar.game.behavior.wander import Wander

from NudWar.utils.pumpy import *

import math

class NudManager:
	def __init__(self, map: Map, camera: Camera, window: Window, ran: LCG, constants: Constants):
		self.map = map
		self.camera = camera
		self.window = window
		self.ran = ran
		self.constants = constants
	
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
	
	# entry
	
	def Entry(self, nud: Nud, currentRegion: Region):
		if len(nud.actionQueue) < 1:
			nud.AddNewAction(Wander(nud, self.ran))
		action: Action = nud.actionQueue[-1]
		if action.Update(self.window.gameTime) == Action.COMPLETED:
			nud.RemoveLastAction()