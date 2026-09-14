from NudWar.game.gameObject import GameObject

class Action(GameObject):
	"""
	Basic component of tasks. Actions can run in real time.
	"""
	def __init__(self):
		super().__init__()