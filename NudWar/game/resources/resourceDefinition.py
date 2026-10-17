from NudWar.game.gameObject import GameObject

class ResourceDefinition(GameObject):
	def __init__(self, name: str):
		super().__init__()
		self.name = name