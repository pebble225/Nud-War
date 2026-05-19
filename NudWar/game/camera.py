from NudWar.game.transformGameObject import TransformGameObject

class Camera(TransformGameObject):
	def __init__(self):
		super().__init__()

		self.moveSpeed = 10.0
	
	def NudgeCamera(self, x: float, y: float):
		self.Nudge(x * self.moveSpeed, y*self.moveSpeed)