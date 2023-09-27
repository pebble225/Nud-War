import pygame
import math
import numpy
import random

window = None
running = True

instance = []

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

#could this be merged with other classes like Resource?
class Projectile:
	pass


class Camera:
	pos = [0.0, 0.0]
	scale = 1.0
	screenOffset = (dim[0] / 2, dim[1] / 2)


class Nud:
	TYPE_COMBAT = 0
	TYPE_TRADING = 100
	TYPE_CONSTRUCTION = 200
	TYPE_GATHERING = 300

	def __init__(self, faction: Faction, pos: list[float, float], nudType: int):
		self.faction = faction
		self.pos = pos
		self.type = nudType
		self.rotation = [1.0, 0]
		self.speed = 2
		self.scale = 5
		self.turnSpeed = 3
		self.orders = []

		#maybe replace if else chain in the future

		if nudType == Nud.TYPE_COMBAT:
			self.meshFunction = Mesh.GetCombatNud
		elif nudType == Nud.TYPE_TRADING:
			self.meshFunction = Mesh.GetTradingNud
		elif nudType == Nud.TYPE_CONSTRUCTION:
			self.meshFunction = Mesh.GetConstructionNud
		elif nudType == Nud.TYPE_GATHERING:
			self.meshFunction = Mesh.GetGatheringNud
		else:
			self.meshFunction = None


class AdminAI:
	def CommandNud(nud: Nud, orderType):
		o = Order()
		o.SetType(orderType)
		nud.orders.append(o)


	def NudCommand_addPosition(self, x, y, index = 0):
		self.orders[index].positions.append([x, y])


	def NudCommand_removeOrder(self, o):
		if o in self.orders:
			self.orders.remove(o)
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
		targetDistance = numpy.sqrt((nud.pos[0] - targetPos[0]) ** 2 + (nud.pos[1] - targetPos[1]) ** 2)
		targetVector = GetAngleVectorToPoint(nud.pos, targetPos)
		differenceAngle = GetVectorAngleDifference(nud.rotation, targetVector) * 180 / numpy.pi

		if PointsInRange(nud.pos, targetPos):
			nud.orders.pop(0)
			return
		if differenceAngle < -GOTO_TARGET_ROTATION_TOLERANCE or differenceAngle > GOTO_TARGET_ROTATION_TOLERANCE:
			SmartNudAI.TurnByReferenceAngle(nud, differenceAngle)
			return
		SmartNudAI.MoveForward(nud, targetDistance)
	
	def MoveForward(nud: Nud, distance):
		if distance > nud.speed:
			distance = nud.speed
		
		nud.pos[0] += nud.rotation[0] * distance
		nud.pos[1] += nud.rotation[1] * distance
	

	def TurnLeft(nud: Nud, degrees: float):
		if degrees > nud.turnSpeed:
			degrees = nud.turnSpeed
		change = GetAngleVector(-degrees)
		nud.rotation = [nud.rotation[0]*change[0]-nud.rotation[1]*change[1], nud.rotation[0]*change[1]+nud.rotation[1]*change[0]]
		Spatial.NormalizeNudRotation(nud)


	def TurnRight(nud: Nud, degrees: float):
		if degrees > nud.turnSpeed:
			degrees = nud.turnSpeed
		change = GetAngleVector(degrees)
		nud.rotation = [nud.rotation[0]*change[0]-nud.rotation[1]*change[1], nud.rotation[0]*change[1]+nud.rotation[1]*change[0]]
		Spatial.NormalizeNudRotation(nud)
	

	def TurnByReferenceAngle(nud: Nud, angle: float):
		updatedAngle = numpy.clip(angle, -nud.turnSpeed, nud.turnSpeed)
		turningVector = GetAngleVector(updatedAngle)
		nud.rotation = [nud.rotation[0]*turningVector[0]-nud.rotation[1]*turningVector[1], nud.rotation[0]*turningVector[1]+nud.rotation[1]*turningVector[0]]
		Spatial.NormalizeNudRotation(nud)
	
	# Combat Orders
	# Trade Orders
	# Build Orders
	# Gathering Orders
		


class DumbNudAI:
	pass

Order.Lookup[Order.TYPE_GOTO] = SmartNudAI.Goto


class Renderer:
	#consider making more generic function to render all meshes
	def RenderNud(nud: Nud):
		global GLOBAL_Y_INVERT

		mesh = nud.meshFunction()

		for i in range(0, len(mesh), 1):
			mesh[i][0] *= nud.scale
			mesh[i][1] *= nud.scale

			x1 = mesh[i][0]
			y1 = mesh[i][1]

			mesh[i][0] = x1*nud.rotation[0] - y1*nud.rotation[1]
			mesh[i][1] = y1*nud.rotation[0] + x1*nud.rotation[1]

			mesh[i][0] += nud.pos[0]
			mesh[i][1] += nud.pos[1]

			mesh[i][0] -= Camera.pos[0]
			mesh[i][1] -= Camera.pos[1]

			mesh[i][1] *= GLOBAL_Y_INVERT

			mesh[i][0] *= Camera.scale
			mesh[i][1] *= Camera.scale

			mesh[i][0] += Camera.screenOffset[0]
			mesh[i][1] += Camera.screenOffset[1]

		pygame.draw.polygon(window, nud.faction.color, mesh)


class Spatial:
	#Chunk Count describes the width and height of the chunk block. Please keep it even. Pretty please
	ChunkCount = 40
	ChunkSize = 1000

	MaxChunkIndex = int(ChunkCount / 2 - 1)
	MinChunkIndex = int(-ChunkCount / 2)

	chunks = {}

	def InitializeChunks():
		for y in numpy.arange(-Spatial.ChunkCount/2, Spatial.ChunkCount/2, 1):
			for x in numpy.arange(-Spatial.ChunkCount/2, Spatial.ChunkCount/2, 1):
				Spatial.chunks[(x, y)] = []

	def NormalizeNudRotation(nud: Nud):
		d = math.sqrt(nud.rotation[0] ** 2 + nud.rotation[1] ** 2)
		nud.rotation = [nud.rotation[0] / d, nud.rotation[1] / d]

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
	global instance, fac, n, dim

	Spatial.InitializeChunks()

	fac = Faction("Team Blue", (0,100,255))

	print(Spatial.GetChunkCoordinate((1024.0, -35.0)))

	for i in range(0, 100, 1):
		#n = Nud(fac, [random.randint(0, dim[0]), random.randint(0, dim[1])], 0)
		n = Nud(fac, [random.randint(-dim[0]/2, dim[0]/2), random.randint(-dim[1]/2, dim[1]/2)], Nud.TYPE_COMBAT)
		instance.append(n)

		AdminAI.CommandNud(n,Order.TYPE_GOTO)
		AdminAI.NudCommand_addPosition(n, random.randint(-dim[0]/2, dim[0]/2), random.randint(-dim[1]/2, dim[1]/2))

		AdminAI.CommandNud(n,Order.TYPE_GOTO)
		AdminAI.NudCommand_addPosition(n, random.randint(-dim[0]/2, dim[0]/2), random.randint(-dim[1]/2, dim[1]/2), 1)

def Update():
	global instance

	#step 1: Run spatial abstract to update nud math (might not need this step)

	#step 2: run the diplomat AI

	#step 3: run the Nud AI and Dumb AI

	for nud in instance:
		SmartNudAI.UpdateNud(nud)


def Render():
	global window, instance, fac, n

	window.fill((0, 0, 0))

	for nud in instance:
		Renderer.RenderNud(nud)

	pygame.display.flip()


def main():
	global window, running, dim

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
			delta -= 1.0
		
		if pygame.time.get_ticks() - lastFrame > frameNS:
			Render()
			lastFrame += frameNS


	pygame.quit()


if __name__ == "__main__":
	main()
