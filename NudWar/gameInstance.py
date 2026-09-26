import pygame

from NudWar.game.camera import Camera
from NudWar.game.map import Map
from NudWar.game.nud import Nud
from NudWar.game.transformGameObject import TransformGameObject
from NudWar.game.constants import Constants

from NudWar.game.behavior.moveTo import MoveTo
from NudWar.game.behavior.idle import Idle

from NudWar.input.playerController import PlayerController
from NudWar.utils.rng import RNG, LCG

from NudWar.render.renderer import Renderer
from NudWar.manager.nudManager import NudManager
from NudWar.manager.regionManager import RegionManager
from NudWar.manager.mapManager import MapManager

from NudWar.render.window import Window

class GameInstance:
	def __init__(self):
		self.window: Window = Window()
		self.camera: Camera = Camera()
		self.camera.name = "camera"
		self.camera.SetScale(10.0)
		self.playerController: PlayerController = PlayerController()
		self.playerController.SetTarget(self.camera)
		self.map: Map = Map()
		self.ran = LCG.NADS64bit()
		self.constants = Constants()

		self.renderer: Renderer = Renderer(self.map, self.window, self.camera)
		self.nudManager: NudManager = NudManager(self.map, self.camera, self.window, self.ran, self.constants)
		self.regionManager: RegionManager = RegionManager(self.nudManager, self.window, self.constants)
		self.mapManager: MapManager = MapManager(self.map, self.regionManager)

		self.target = TransformGameObject()
		self.target.name = "target"
	
	def Start(self):
		for y in range(3):
			for x in range(4):
				self.map.AddRegion(x, y)
		for i in range(50):
			self.regionManager.CreateBasicNud(self.map.GetRegion(0, 0), 40, 40)
	
	def Input(self):
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				self.window.running = False
			self.playerController.RegisterEvent(e)

	def Update(self):
		self.playerController.Update()

		self.mapManager.UpdateAll()

	def main(self):
		pygame.init()

		self.window.Init()

		actualTPS = 0

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
			tickDelta += float(nowTime-lastTime) / self.constants.MSPerTick
			lastTime = nowTime

			while not (tickDelta < 1):
				self.Update()
				self.window.gameTime += 1
				actualTPS += 1
				tickDelta -= 1.0
			
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