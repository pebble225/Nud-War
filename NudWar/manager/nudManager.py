from NudWar.game.nud import Nud
from NudWar.game.map import Map
from NudWar.game.camera import Camera
from NudWar.game.region import Region

from NudWar.utils.pumpy import *

class NudManager:
	def __init__(self, map: Map, camera: Camera):
		self.map = map
		self.camera = camera
	
	# Layer 1

	def MoveForward(self, nud: Nud, distance: float):
		moveSpeed = nud.GetMoveSpeed()
		distance = moveSpeed if distance > moveSpeed else distance
		nud.MoveForward()
	
	def TurnRight(self, nud: Nud, amount: float):
		rotationSpeed = nud.GetRotationSpeed()
		amount = rotationSpeed if amount > rotationSpeed else amount
		nud.RotateByAngle(amount)
	
	def TurnLeft(self, nud: Nud, amount: float):
		rotationSpeed = nud.GetRotationSpeed()
		amount = rotationSpeed if amount > rotationSpeed else amount
		nud.RotateByAngle(-amount)
	
	def TurnRightMax(self, nud: Nud):
		nud.RotateByAngle(nud.rotationSpeed)
	
	def TurnLeftMax(self, nud: Nud):
		nud.RotateByAngle(-nud.rotationSpeed)

	# Layer 2

	
	
	# Layer 3

	def MoveToPosition(self, nud: Nud, currentRegion: Region, pos: tuple[float]):
		"""
		@param pos Relative to position of the current region
		"""

		
	
	# entry
	
	def Entry(self, nud: Nud, currentRegion: Region):
		self.TurnRightMax(nud)