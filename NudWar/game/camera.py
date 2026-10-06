from NudWar.game.transformGameObject import TransformGameObject

from NudWar.data.dataBase import DataBase
from NudWar.data.unitData import UnitData

class Camera(TransformGameObject):
	def __init__(self, database: DataBase):
		super().__init__()

		self.prevPos = None
		self.moveSpeed = database.unitData.ToMetersPerTick(100.0)
	
	def NudgeCamera(self, x: float, y: float):
		#self.prevPos = list(self.pos)
		self.Nudge(x * self.moveSpeed, y*self.moveSpeed)

		#interpPos = [lerp(self.pos[0], self.nextPos[0], deltaValue), lerp(self.pos[1], self.nextPos[1], deltaValue)]