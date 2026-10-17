from NudWar.game.gameObject import GameObject

class Faction(GameObject):
	def __init__(self, color: tuple[int, int, int]):
		super().__init__()

		self.color = color