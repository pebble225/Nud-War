class RenderData:
	def __init__(self):
		self.PORTAL_TENDRIL_WIDTH = 0.5 # meters
		self.PORTAL_TENDRIL_LENGTH = 2.0 # meters

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