import pygame
import math
import numpy
import random

window = None
running = True

NudInstance = []

dim = (1600,900)

GLOBAL_Y_INVERT = -1.0

class Mesh:
	#factory function ensures a new instance of the mesh that can be adjusted.

	"""
	
	mesh [
		[vertex0.x, vertex0.y] , [vertex1.x, vertex1.y], ...
	]

	"""

	def GetCombatNud():
		return [
			[1.0, 0], [-1.0, 1.0], [-0.5, 0], [-1.0, -1.0]
		]
	def GetTradingNud():
		return [
			[0.5, 1.0], [1.0, 0.0], [0.5, -1.0], [-1.0, -1.0], [-0.5, 0.0], [-1.0, 1.0]
		]
	def GetConstructionNud():
		return [
			[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-0.5, 0.0], [-1.0, 1.0]
		]
	def GetGatheringNud():
		return [
			[1.0, 1.0], [1.0, 0.75], [0.5, 0.75], [0.5, -0.75], [1.0, -0.75], [1.0, -1.0], [-1.0, -1.0], [-0.5, 0.0], [-1.0, 1.0]
		]
	def GetRock():
		return [
			[1.0, 1.0], [0.6, 0.3], [0.6, -0.3], [1.0, -1.0], [0.3, -0.6], [-0.3, -0.6], [-1.0, -1.0], [-0.6, -0.3], [-0.6, 0.3], [-1.0, 1.0], [-0.3, 0.6]
		]


class Faction:
	nextID = 0

	def __init__(self, name, color):
		self.id = Faction.nextID
		self.name = name
		self.color = color

		self.totalNuds = 0
		self.totalCombatNuds = 0
		self.totalTradingNuds = 0
		self.totalConstructionNuds = 0
		self.totalGatheringNuds = 0
		

		Faction.nextID += 1


class Order:

	#maybe make the constants more pythonic eventually
	TYPE_GOTO = 0

	TYPE_ATTACK = 100
	
	TYPE_TRANSPORT = 200

	#Order.Lookup contains and array of functions that correspond to order codes

	Lookup = [None] * 1000

	def __init__(self):
		self.orderType = None
		self.positions = []
		self.targets = []
		self.distances = []
	

	#functions that directly change data in class will stay in that class
	def SetType(self, orderType):
		self.orderType = orderType
	

	def AddPosition(self, x, y):
		self.positions.append([x, y])
	

	def AddTarget(self, t):
		self.targets.append(t)


class Rock:
	GlobalAngleOffset = [1.0, 0.0]

	CurrentTotalRocks = 0

	ROCK_DENSITY = 10
	ROCK_TOTAL = None
	ROCK_SPAWN_DELAY = 30

	RockTimer = 0

	def __init__(self, pos):
		self.transform = Transform(pos, [1.0, 0.0], [5.0, 5.0], [100, 100, 100])
		self.transform.meshFunction = Mesh.GetRock

		Rock.CurrentTotalRocks += 1

	
	#Desire to practice avoiding two way referencing
	def SetRockTotal(total: int):
		Rock.ROCK_TOTAL = total

class Projectile:
	pass


class Camera:
	pos = [0.0, 0.0]
	scale = 1.0
	screenOffset = (dim[0] / 2, dim[1] / 2)


class Transform:
	def __init__(self, pos: list[float, float], rotation: list[float, float], scale: list[float, float], color: list[int, int, int]):
		self.pos = pos
		self.rotation = rotation
		self.scale = scale
		self.meshFunction = None
		self.color = color


class Nud:
	TYPE_COMBAT = 0
	TYPE_TRADING = 100
	TYPE_CONSTRUCTION = 200
	TYPE_GATHERING = 300

	NEXT_NUD_ID = 0

	def __init__(self, faction: Faction, pos: list[float, float], nudType: int):
		self.faction = faction
		self.type = nudType

		self.transform = Transform(pos, [1.0, 0.0], [5.0, 5.0], faction.color)
		self.speed = 2
		self.turnSpeed = 3
		self.orders = []
		self.currentChunk = None
		self.targetChunk = None
		self.ID = Nud.NEXT_NUD_ID
		Nud.NEXT_NUD_ID += 1

		#maybe replace if else chain in the future

		if nudType == Nud.TYPE_COMBAT:
			self.transform.meshFunction = Mesh.GetCombatNud
		elif nudType == Nud.TYPE_TRADING:
			self.transform.meshFunction = Mesh.GetTradingNud
		elif nudType == Nud.TYPE_CONSTRUCTION:
			self.transform.meshFunction = Mesh.GetConstructionNud
		elif nudType == Nud.TYPE_GATHERING:
			self.transform.meshFunction = Mesh.GetGatheringNud
		else:
			self.meshFunction = None


class AdminAI:
	def CommandNud(nud: Nud, orderType):
		o = Order()
		o.SetType(orderType)
		nud.orders.append(o)


	def NudCommand_addPosition(nud, x, y, index = 0):
		nud.orders[index].positions.append([x, y])


	def NudCommand_removeOrder(nud, o):
		if o in nud.orders:
			nud.orders.remove(o)
		else:
			print("Tried to remove order from Nud that is not in order list.")


GOTO_TARGET_ROTATION_TOLERANCE = 1.0

class SmartNudAI:
	def UpdateNud(nud):
		if len(nud.orders) > 0:
			Order.Lookup[nud.orders[0].orderType](nud)

	# Global Orders

	def Goto(nud: Nud):
		global GOTO_TARGET_ROTATION_TOLERANCE

		if len(nud.orders[0].positions) < 1:
			print("A goto order was given without a position.")
			return
		
		targetPos = nud.orders[0].positions[0]
		targetDistance = numpy.sqrt((nud.transform.pos[0] - targetPos[0]) ** 2 + (nud.transform.pos[1] - targetPos[1]) ** 2)
		targetVector = GetAngleVectorToPoint(nud.transform.pos, targetPos)
		differenceAngle = GetVectorAngleDifference(nud.transform.rotation, targetVector) * 180 / numpy.pi

		if PointsInRange(nud.transform.pos, targetPos):
			nud.orders.pop(0)
			return
		if differenceAngle < -GOTO_TARGET_ROTATION_TOLERANCE or differenceAngle > GOTO_TARGET_ROTATION_TOLERANCE:
			SmartNudAI.TurnByReferenceAngle(nud, differenceAngle)
			return
		SmartNudAI.MoveForward(nud, targetDistance)

	def DetermineNudChunkChange(nud: Nud):
		chunk = Spatial.GetChunkCoordinate(nud.transform.pos)
		if chunk != nud.currentChunk:
			nud.targetChunk = chunk
			Spatial.AppendNud(nud)
	
	def MoveForward(nud: Nud, distance):
		if distance > nud.speed:
			distance = nud.speed
		
		nud.transform.pos[0] += nud.transform.rotation[0] * distance
		nud.transform.pos[1] += nud.transform.rotation[1] * distance

		SmartNudAI.DetermineNudChunkChange(nud)
	

	def TurnLeft(nud: Nud, degrees: float):
		if degrees > nud.turnSpeed:
			degrees = nud.turnSpeed
		change = GetAngleVector(-degrees)
		nud.transform.rotation = [nud.transform.rotation[0]*change[0]-nud.transform.rotation[1]*change[1], nud.transform.rotation[0]*change[1]+nud.transform.rotation[1]*change[0]]
		Spatial.NormalizeNudRotation(nud)


	def TurnRight(nud: Nud, degrees: float):
		if degrees > nud.turnSpeed:
			degrees = nud.turnSpeed
		change = GetAngleVector(degrees)
		nud.transform.rotation = [nud.transform.rotation[0]*change[0]-nud.transform.rotation[1]*change[1], nud.transform.rotation[0]*change[1]+nud.transform.rotation[1]*change[0]]
		Spatial.NormalizeNudRotation(nud)
	

	def TurnByReferenceAngle(nud: Nud, angle: float):
		updatedAngle = numpy.clip(angle, -nud.turnSpeed, nud.turnSpeed)
		turningVector = GetAngleVector(updatedAngle)
		nud.transform.rotation = [nud.transform.rotation[0]*turningVector[0]-nud.transform.rotation[1]*turningVector[1], nud.transform.rotation[0]*turningVector[1]+nud.transform.rotation[1]*turningVector[0]]
		Spatial.NormalizeNudRotation(nud)
	
	# Combat Orders
	# Trade Orders
	# Build Orders
	# Gathering Orders
		


class DumbNudAI:
	pass

Order.Lookup[Order.TYPE_GOTO] = SmartNudAI.Goto



class Renderer:
	def RenderChunksNearCamera():
		CAMERA_CHUNK_RANGE = 3

		cameraChunk = Spatial.GetChunkCoordinate(Camera.pos)

		for y in range(cameraChunk[1]-CAMERA_CHUNK_RANGE, cameraChunk[1]+CAMERA_CHUNK_RANGE, 1):
			for x in range(cameraChunk[0]-CAMERA_CHUNK_RANGE, cameraChunk[0]+CAMERA_CHUNK_RANGE, 1):
				if Spatial.isValidChunk((x, y)):
					for obj in Spatial.chunks[(x, y)]:
						Renderer.RenderTransform(obj.transform)

	def RenderTransform(transform: Transform):
		global GLOBAL_Y_INVERT 

		mesh = transform.meshFunction()

		for i in range(0, len(mesh), 1):
			mesh[i][0] *= transform.scale[0]
			mesh[i][1] *= transform.scale[1]

			x1 = mesh[i][0]
			y1 = mesh[i][1]

			mesh[i][0] = x1*transform.rotation[0] - y1*transform.rotation[1]
			mesh[i][1] = y1*transform.rotation[0] + x1*transform.rotation[1]

			mesh[i][0] += transform.pos[0]
			mesh[i][1] += transform.pos[1]

			mesh[i][0] -= Camera.pos[0]
			mesh[i][1] -= Camera.pos[1]

			mesh[i][1] *= GLOBAL_Y_INVERT

			mesh[i][0] *= Camera.scale
			mesh[i][1] *= Camera.scale

			mesh[i][0] += Camera.screenOffset[0]
			mesh[i][1] += Camera.screenOffset[1]

		pygame.draw.polygon(window, transform.color, mesh)


class Spatial:
	#Chunk Count describes the width and height of the chunk block. Please keep it even. Pretty please
	ChunkCount = 40
	ChunkSize = 1000
	MaxLeft = 0
	MaxRight = ChunkCount*ChunkSize-1
	MaxUp = ChunkCount*ChunkSize-1
	MaxDown = 0

	chunks = {}

	NudChunkShiftQueue = []

	#hmmm bloat all of the operators with start and update functions?
	def Start():
		Spatial.InitializeChunks()

		Rock.SetRockTotal(Rock.ROCK_DENSITY * Spatial.ChunkCount * Spatial.ChunkCount)


	def Update():
		Spatial.ShiftNudChunks()

		Rock.RockTimer += 1

		if Rock.RockTimer >= Rock.ROCK_SPAWN_DELAY:
			Rock.RockTimer -= Rock.ROCK_SPAWN_DELAY
			if Rock.CurrentTotalRocks < Rock.ROCK_TOTAL:
				rock = Rock((random.randrange(Spatial.MaxLeft, Spatial.MaxRight), random.randrange(Spatial.MaxUp)))
				Spatial.AssignStationaryToChunk(rock)
				print(Rock.CurrentTotalRocks)
			


	def isValidChunk(chunk: tuple[int, int]) -> bool:
		if chunk[0] < 0 or chunk[0] > Spatial.ChunkCount-1:
			return False
		elif chunk[1] < 0 or chunk[1] > Spatial.ChunkCount-1:
			return False
		else:
			return True

	def AppendNud(nud: Nud):
		Spatial.NudChunkShiftQueue.append(nud)

	#there are currently no handles for nuds outside of chunks, so if an invalid position is used to look up, it will return a KeyError
	def ShiftNudChunks():
		for nud in Spatial.NudChunkShiftQueue:
			Spatial.chunks[nud.targetChunk].append(nud)
			Spatial.chunks[nud.currentChunk].remove(nud)
			nud.currentChunk = nud.targetChunk
			nud.targetChunk = None
		Spatial.NudChunkShiftQueue = []

	#this should only be used for newly initialized nuds
	def AssignNudToChunk(nud:Nud):
		nud.currentChunk = Spatial.GetChunkCoordinate(nud.transform.pos)
		Spatial.chunks[nud.currentChunk].append(nud)

	def AssignStationaryToChunk(obj):
		chunk = Spatial.GetChunkCoordinate(obj.transform.pos)
		if Spatial.isValidChunk(chunk):
			Spatial.chunks[chunk].append(obj)

	def InitializeChunks():
		for y in numpy.arange(0, Spatial.ChunkCount, 1):
			for x in numpy.arange(0, Spatial.ChunkCount, 1):
				Spatial.chunks[(x, y)] = []

	def NormalizeRotation(rot: list[float, float]):
		d = math.sqrt(rot[0] ** 2 + rot[1] ** 2)
		rot = [rot[0] / d, rot[1] / d]

	#get rid of this and use generic normalize function
	def NormalizeNudRotation(nud: Nud):
		d = math.sqrt(nud.transform.rotation[0] ** 2 + nud.transform.rotation[1] ** 2)
		nud.transform.rotation = [nud.transform.rotation[0] / d, nud.transform.rotation[1] / d]

	def GetChunkCoordinate(pos: list[float, float]) -> tuple[int, int]:
		return (int(MoveValueLeft(pos[0], Spatial.ChunkSize) / Spatial.ChunkSize), int(MoveValueLeft(pos[1], Spatial.ChunkSize) / Spatial.ChunkSize))


def PointsInRange(pos1: tuple[float, float], pos2: tuple[float, float], tolerance: float = 0.1):
	return pos1[0] > pos2[0] - tolerance and pos1[0] < pos2[0] + tolerance and pos1[1] > pos2[1] - tolerance and pos1[1] < pos2[1] + tolerance


def GetAngleVectorToPoint(originPos: tuple[float, float], targetPos: tuple[float, float]) -> list[float, float]:
	diffX = targetPos[0] - originPos[0]
	diffY = targetPos[1] - originPos[1]
	d = math.sqrt(diffX ** 2 + diffY ** 2)
	if d == 0:
		return [1.0, 0.0]
	return [diffX / d, diffY / d]


def GetAngleVector(angle: float) -> list[float, float]:
	return [math.cos(angle*math.pi/180.0), math.sin(angle*math.pi/180.0)]


def MoveValueLeft(n: float, g: int) -> float:
	return n - (n % g)


"""

Moderately understood use of trigonometery to get the angle between two vectors.
ArcTan2 is used to avoid extremely large values associated with Tangent.

"""
def GetVectorAngleDifference(vec1: tuple[float, float], vec2: tuple[float, float]) -> float:
	return numpy.arctan2(vec1[0]*vec2[1]-vec1[1]*vec2[0], vec1[0]*vec2[0]+vec1[1]*vec2[1])


def Input():
	global window, running

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False


fac = None

def Start():
	global NudInstance, fac, n, dim

	Spatial.Start()

	fac = Faction("Team Blue", (0,100,255))

	for i in range(0, Rock.ROCK_TOTAL, 1):
		rock = Rock((random.randrange(Spatial.MaxLeft, Spatial.MaxRight), random.randrange(Spatial.MaxUp)))
		Spatial.AssignStationaryToChunk(rock)

	"""
	n = Nud(fac, [0.0, 0.0], Nud.TYPE_BLAH)
	NudInstance.append(n)
	Spatial.AssignNudToChunk(n)
	"""

def Update():
	global NudInstance

	Spatial.Update()

	Camera.pos = [Camera.pos[0] + 1, Camera.pos[1] + 1]

	#step 1: Run spatial abstract to update nud math (might not need this step)

	#step 2: run the diplomat AI

	#step 3: run the Nud AI and Dumb AI

	for nud in NudInstance:
		SmartNudAI.UpdateNud(nud)
		

def Render():
	global window, NudInstance, fac, n

	window.fill((0, 0, 0))

	Renderer.RenderChunksNearCamera()

	"""
	for nud in NudInstance:
		Renderer.RenderNud(nud)
	"""
	pygame.display.flip()


gameRuntime = 0


def main():
	global window, running, dim, gameRuntime

	pygame.init()

	window = pygame.display.set_mode(dim)

	tps = 60
	ns = 1000.0 / tps

	fps = 30
	frameNS = 1000.0 / fps

	delta = 0.0

	lastTime = pygame.time.get_ticks()
	lastFrame = pygame.time.get_ticks()

	Start()

	#yea I don't wanna recaulculate this very specific float value so I'll store it >:(
	oneFloat = 0.9999999999

	while running:
		Input()

		nowTime = pygame.time.get_ticks()
		delta += (nowTime - lastTime) / ns
		lastTime = nowTime

		while (delta > oneFloat):
			Update()
			gameRuntime += 1
			delta -= 1.0
		
		if pygame.time.get_ticks() - lastFrame > frameNS:
			Render()
			lastFrame += frameNS


	pygame.quit()


if __name__ == "__main__":
	main()
