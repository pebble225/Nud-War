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
	#factory function ensures a new instance of the mesh that can be adjusted. There is only one mesh so this is the method that will be used
	#for multiple meshes make mesh class or make a factory function for each mesh

	"""
	
	mesh [
		[vertex0.x, vertex0.y] , [vertex1.x, vertex1.y], ...
	]

	"""

	def GetStandardNud():
		return [
			[1.0, 0], [-1.0, 1.0], [-0.5, 0], [-1.0, -1.0]
		]


class Faction:
	nextID = 0

	def __init__(self, name, color):
		self.id = Faction.nextID
		self.name = name
		self.color = color

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

# I'm divided on doing this way but I don't think Python likes me putting factories in the class definition
# Factory class exists to keep Nud constructor uncomplicated
class NudFactory:
	def CombatNud(faction: Faction, pos: list[float, float]) -> Nud:
		return Nud(faction, pos, Nud.TYPE_COMBAT)
	def TradingNud(faction: Faction, pos: list[float, float]) -> Nud:
		return Nud(faction, pos, Nud.TYPE_TRADING)
	def ConstructionNud(faction: Faction, pos: list[float, float]) -> Nud:
		return Nud(faction, pos, Nud.TYPE_CONSTRUCTION)
	def GatheringNud(faction: Faction, pos: list[float, float]) -> Nud:
		return Nud(faction, pos, Nud.TYPE_GATHERING)


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
	def RenderNud(nud: Nud):
		mesh = Mesh.GetStandardNud()

		for i in range(0, len(mesh), 1):
			mesh[i][0] *= nud.scale
			mesh[i][1] *= nud.scale

			x1 = mesh[i][0]
			y1 = mesh[i][1]

			mesh[i][0] = x1*nud.rotation[0] - y1*nud.rotation[1]
			mesh[i][1] = y1*nud.rotation[0] + x1*nud.rotation[1]

			mesh[i][0] += nud.pos[0]
			mesh[i][1] += nud.pos[1]

		pygame.draw.polygon(window, nud.faction.color, mesh)


class Spatial:
	def NormalizeNudRotation(nud: Nud):
		d = math.sqrt(nud.rotation[0] ** 2 + nud.rotation[1] ** 2)
		nud.rotation = [nud.rotation[0] / d, nud.rotation[1] / d]


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

	fac = Faction("Team Blue", (0,100,255))

	for i in range(0, 100, 1):
		#n = Nud(fac, [random.randint(0, dim[0]), random.randint(0, dim[1])], 0)
		n = NudFactory.CombatNud(fac, [random.randint(0, dim[0]), random.randint(0, dim[1])])
		instance.append(n)

		AdminAI.CommandNud(n,Order.TYPE_GOTO)
		AdminAI.NudCommand_addPosition(n, random.randint(0, dim[0]), random.randint(0, dim[1]))

		AdminAI.CommandNud(n,Order.TYPE_GOTO)
		AdminAI.NudCommand_addPosition(n, random.randint(0, dim[0]), random.randint(0, dim[1]), 1)

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
	ns = 1000 / tps

	delta = 0

	lastTime = pygame.time.get_ticks()

	Start()

	while running:
		Input()

		nowTime = pygame.time.get_ticks()
		delta += (nowTime - lastTime) / ns
		lastTime = nowTime

		while (delta > 0.9999999):
			Update()
			delta -= 1.0
		
		Render()


	pygame.quit()


if __name__ == "__main__":
	main()
