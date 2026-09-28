import numpy as np
from NudWar.utils.pumpy import *

from NudWar.data.unitData import UnitData

class RenderData:
	def __init__(self, unitData: UnitData):
		self.unitData = unitData

		#PORTAL MESH
		self.PORTAL_TENDRIL_WIDTH = 0.5 # meters
		self.PORTAL_TENDRIL_LENGTH = 2.0 # meters
		self.PORTAL_EPICENTER_RADIUS = 0.6 # meters

		self.PORTAL_CW_TENDRIL_ANGLE_VELOCITY = 180 # degrees/second
		self.PORTAL_CCW_TENDRIL_ANGLE_VELOCITY = -360 # degrees/second

		self.PORTAL_CW_TENDRIL_VECTOR = [np.cos(np.radians(unitData.ToDegreesPerTick(self.PORTAL_CW_TENDRIL_ANGLE_VELOCITY))), np.sin(np.radians(unitData.ToDegreesPerTick(self.PORTAL_CW_TENDRIL_ANGLE_VELOCITY)))]
		self.PORTAL_CCW_TENDRIL_VECTOR = [np.cos(np.radians(unitData.ToDegreesPerTick(self.PORTAL_CCW_TENDRIL_ANGLE_VELOCITY))), np.sin(np.radians(unitData.ToDegreesPerTick(self.PORTAL_CCW_TENDRIL_ANGLE_VELOCITY)))]

	def GetBasicNudMesh(self):
		return [
			[-0.30, -0.25],
			[0.35, 0.0],
			[-0.30, 0.25],
			[-0.10, 0.0]
		]

	def GetPortalTendril(self):
		return [
			[0.0, -self.PORTAL_TENDRIL_WIDTH],
			[self.PORTAL_TENDRIL_LENGTH, 0.0],
			[0.0, self.PORTAL_TENDRIL_WIDTH],
			[-self.PORTAL_TENDRIL_LENGTH, 0.0]
		]