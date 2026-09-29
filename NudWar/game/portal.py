from NudWar.game.transformGameObject import TransformGameObject

class Portal(TransformGameObject):
	def __init__(self):
		super().__init__()

		self.destination: Portal = None

	def AddDestination(self, destination: "Portal"):
		self.destination = destination