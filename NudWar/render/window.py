import pygame
from screeninfo import get_monitors

class Window:
	def __init__(self, dim: tuple = None):
		self.instance = None
		self.dim = self.GetPrimaryMonitorResolution() if dim is None else dim
		self.running = True
		self.gameTime = 0
	
	def Init(self):
		self.instance = pygame.display.set_mode(self.dim, pygame.NOFRAME)
	
	def GetInstance(self) -> pygame.surface.Surface:
		return self.instance
	
	def GetPrimaryMonitorResolution(self) -> tuple:
		for m in get_monitors():
			if m.is_primary:
				return (m.width, m.height)
	
	def GetTopLeft(self) -> tuple:
		return (0, 0)
	
	def GetTopRight(self) -> tuple:
		return (self.dim[0], 0)
	
	def GetBottomLeft(self) -> tuple:
		return (0, self.dim[1])
	
	def GetBottomRight(self) -> tuple:
		return self.dim
	
	def GetCenter(self) -> tuple:
		return (self.dim[0] // 2, self.dim[1] // 2)
	
	def GetWidth(self) -> int:
		return self.dim[0]
	
	def GetHeight(self) -> int:
		return self.dim[1]