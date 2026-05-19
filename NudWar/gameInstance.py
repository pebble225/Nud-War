import pygame

from NudWar.game.camera import Camera
from NudWar.game.map import Map

from NudWar.input.playerController import PlayerController

from NudWar.render.renderer import Renderer
from NudWar.render.window import Window

class GameInstance:
	def __init__(self):
		self.window: Window = Window()
		self.camera = Camera()
		self.camera.SetScale(1.0)
		self.playerController = PlayerController()
		self.playerController.SetTarget(self.camera)
		self.map = Map()

		self.renderer = Renderer(self.map, self.window, self.camera)
	
	def Start(self):
		for y in range(3):
			for x in range(4):
				self.map.AddRegion(x, y)
	
	def Input(self):
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				self.window.running = False
			self.playerController.RegisterEvent(e)

	def Update(self):
		self.playerController.Update()

	def main(self):
		pygame.init()

		self.window.Init()

		tps = 60.0
		tickMS = 1000.0 / tps
		actualTPS = 0 # this should be moved to Window so that the renderer can draw the report into the screen

		tickDelta = 0.0

		lastTime = pygame.time.get_ticks()

		fps = 60.0
		frameMS = 1000.0 / fps
		actualFPS = 0

		lastFrame = pygame.time.get_ticks()

		timer = pygame.time.get_ticks()

		reportRefreshRate = False

		self.Start()

		while self.window.running:
			self.Input()

			nowTime = pygame.time.get_ticks()
			tickDelta += float(nowTime-lastTime) / tickMS
			lastTime = nowTime

			while not (tickDelta < 1):
				self.Update()
				self.window.gameTime += 1
				actualTPS += 1
				tickDelta -= 1.0
			
			nowFrame = pygame.time.get_ticks()
			if float(nowFrame-lastFrame) > frameMS:
				lastFrame = nowFrame
				self.renderer.Update()
				actualFPS += 1
			
			nowTimer = pygame.time.get_ticks()
			if nowTimer - timer > 1000:
				timer = nowTimer
				if reportRefreshRate:
					print(f"TPS: {actualTPS}\nFPS: {actualFPS}")
				actualTPS = 0
				actualFPS = 0

		pygame.quit()