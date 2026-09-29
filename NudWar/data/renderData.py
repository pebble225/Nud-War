import numpy as np
from NudWar.utils.pumpy import *

from NudWar.data.unitData import UnitData

class BasicNudPrefab:
	def __init__(self):
		super().__init__()

	def GetMesh(self):
		return [
			[-0.30, -0.25],
			[0.35, 0.0],
			[-0.30, 0.25],
			[-0.10, 0.0]
		]

class PortalPrefab:
	def __init__(self, unitData: UnitData):
		self.rot = [1.0, 0.0]
		self.PORTAL_SPIN_SPEED = 180

		self.PORTAL_TENDRIL_WIDTH = 0.5
		self.PORTAL_TENDRIL_LENGTH = 2.0

		self.PORTAL_EPICENTER_RADIUS = 0.6

		self.PORTAL_TENDRIL_COLOR = (72, 8, 104)
		self.PORTAL_EPICENTER_COLOR = (30, 146, 188)

		self.spin = [np.cos(np.radians(unitData.ToDegreesPerTick(self.PORTAL_SPIN_SPEED))), np.sin(np.radians(unitData.ToDegreesPerTick(self.PORTAL_SPIN_SPEED)))]

	def FixedUpdate(self):
		self.rot = MultiplyVectors(self.rot, self.spin)

	def GetMesh(self):
		return [
			MultiplyVectors([-self.PORTAL_TENDRIL_WIDTH, -self.PORTAL_TENDRIL_WIDTH], self.rot),
			MultiplyVectors([0.0, -self.PORTAL_TENDRIL_LENGTH], self.rot),
			MultiplyVectors([self.PORTAL_TENDRIL_WIDTH, -self.PORTAL_TENDRIL_WIDTH], self.rot),
			MultiplyVectors([self.PORTAL_TENDRIL_LENGTH, 0.0], self.rot),
			MultiplyVectors([self.PORTAL_TENDRIL_WIDTH, self.PORTAL_TENDRIL_WIDTH], self.rot),
			MultiplyVectors([0.0, self.PORTAL_TENDRIL_LENGTH], self.rot),
			MultiplyVectors([-self.PORTAL_TENDRIL_WIDTH, self.PORTAL_TENDRIL_WIDTH], self.rot),
			MultiplyVectors([-self.PORTAL_TENDRIL_LENGTH, 0.0], self.rot)
		]

class RenderData:
	def __init__(self, unitData: UnitData):
		self.unitData = unitData

		self.basicNudPrefab = BasicNudPrefab()
		self.portalPrefab = PortalPrefab(unitData)