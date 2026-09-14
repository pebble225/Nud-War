from NudWar.game.transformGameObject import TransformGameObject

from NudWar.game.nud import Nud

class Region(TransformGameObject):
	SIZE = 100

	def __init__(self, x: float, y: float):
		super().__init__()

		self.SetPosition(x*Region.SIZE, y*Region.SIZE)
		self.index = [int(x), int(y)]
		self.SetScale(Region.SIZE)

		self.objects = []
	
	def CreateBasicNud(self, x: float = 0, y: float = 0):
		nud = Nud(10.0, 1.0)
		nud.SetPosition(x + self.index[0]*Region.SIZE, y + self.index[1]*Region.SIZE)
		self.objects.append(nud)