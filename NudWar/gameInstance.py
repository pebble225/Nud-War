import pygame

from NudWar.game.camera import Camera
from NudWar.game.map import Map
from NudWar.game.nud import Nud
from NudWar.game.transformGameObject import TransformGameObject

from NudWar.game.behavior.nud.moveTo import MoveTo
from NudWar.game.behavior.nud.idle import Idle

from NudWar.input.playerController import PlayerController
from NudWar.utils.rng import RNG, LCG

from NudWar.data.unitData import UnitData
from NudWar.data.renderData import RenderData
from NudWar.data.mapData import MapData
from NudWar.data.behaviorData import BehaviorData
from NudWar.data.dataBase import DataBase

from NudWar.render.renderer import Renderer
from NudWar.manager.nudManager import NudManager
from NudWar.manager.regionManager import RegionManager
from NudWar.manager.mapManager import MapManager

from NudWar.render.window import Window

class GameInstance:
	def __init__(self):

		self.dataBase = DataBase()
		self.unitData = self.dataBase.unitData
		self.renderData = self.dataBase.renderData
		self.mapData = self.dataBase.mapData
		

		self.window: Window = Window()
		self.camera: Camera = Camera()
		self.camera.name = "camera"
		self.camera.SetScale(10.0)
		self.playerController: PlayerController = PlayerController()
		self.playerController.SetTarget(self.camera)
		self.map: Map = Map(self.mapData)
		self.ran = LCG.NADS64bit()

		self.camera.SetPosition(self.mapData.REGION_SIZE*2.0, self.mapData.REGION_SIZE*1.5)

		self.renderer: Renderer = Renderer()
		self.nudManager: NudManager = NudManager()
		self.regionManager: RegionManager = RegionManager()
		self.mapManager: MapManager = MapManager()

		self.renderer.ImportModules(self.map, self.window, self.camera, self.mapManager)
		self.renderer.ImportData(self.dataBase)

		self.nudManager.ImportModules(self.map, self.camera, self.window, self.ran)
		self.nudManager.ImportData(self.dataBase)

		self.regionManager.ImportModules(self.nudManager, self.window)
		self.regionManager.ImportData(self.dataBase)

		self.mapManager.ImportModules(self.map, self.regionManager)
		self.mapManager.ImportData(self.dataBase)

	def BasicMap(self):
		for y in range(3):
			for x in range(4):
				region = self.mapManager.AddRegion(x, y)
				n = self.ran.intRange(1, 10)

				for i in range(n):
					self.regionManager.CreateBasicNud(region, 40, 40)

		self.mapManager.LinkHorizontal((0,0),(1,0))
		self.mapManager.LinkVertical((1,0),(1,1))
		self.mapManager.LinkVertical((1,1),(1,2))
		self.mapManager.LinkHorizontal((0,2),(1,2))
		self.mapManager.LinkVertical((0,1),(0,2))
		self.mapManager.LinkVertical((0,0),(0,1))

		self.mapManager.LinkHorizontal((1, 1), (2, 1))

		self.mapManager.LinkVertical((2, 0), (2, 1))
		self.mapManager.LinkHorizontal((2, 0), (3, 0))
		self.mapManager.LinkVertical((3, 0), (3, 1))
		self.mapManager.LinkVertical((3, 1), (3, 2))
		self.mapManager.LinkHorizontal((2, 2), (3, 2))
		self.mapManager.LinkVertical((2, 1), (2, 2))

		self.mapManager.GeneratePortals()
	
	def Start(self):
		self.BasicMap()
	
	def Input(self):
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				self.window.running = False
			self.playerController.RegisterEvent(e)

	def Update(self):
		self.playerController.Update()

		self.renderer.FixedUpdate()

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

		reportRefreshRate = False #this needs to be moved to constants

		self.Start()

		fpsList = []
		def fpsAverage(fpsList: list[int]):
			n = 0
			for i in fpsList:
				n += i
			return int(float(n) / float(len(fpsList)))


		while self.window.running:
			self.Input()

			nowTime = pygame.time.get_ticks()
			tickDelta += float(nowTime-lastTime) / self.unitData.MSPerTick
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
					fpsList.append(actualFPS)
					while len(fpsList) > 60:
						fpsList.pop(0)
					print(f"TPS: {actualTPS}\nFPS: {actualFPS}\nAvg FPS: {fpsAverage(fpsList)}")
				actualTPS = 0
				actualFPS = 0

		pygame.quit()
