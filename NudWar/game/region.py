from NudWar.game.transformGameObject import TransformGameObject

class Region(TransformGameObject):
	SIZE = 100

	def __init__(self, x: float, y: float):
		super().__init__()

		self.SetPosition(x*Region.SIZE, y*Region.SIZE)
		self.index = [int(x), int(y)]
		self.SetScale(Region.SIZE)