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

	def getStandardNud():
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
	TYPE_GOTO = 0
	TYPE_GOTO_RELATIVE = 1

	TYPE_ATTACK = 100
	
	TYPE_TRANSPORT = 200

	#Order.Lookup contains and array of functions that correspond to order codes

	Lookup = [None] * 1000

	def __init__(self):
		self.orderType = None
		self.positions = []
		self.targets = []
	
	def setType(self, orderType):
		self.orderType = orderType
	

	def addPosition(self, x, y):
		self.positions.append([x, y])
	

	def addTarget(self, t):
		self.targets.append(t)


class Nud:
	scale = 5

	def __init__(self, faction, pos, nudType):
		self.faction = faction
		self.pos = pos
		self.type = nudType
		self.rotation = [1.0, 0]
		self.speed = 2
		self.turnSpeed = 3
		self.orders = []

	def Render(self):
		mesh = Mesh.getStandardNud()

		for i in range(0, len(mesh), 1):
			mesh[i][0] *= Nud.scale
			mesh[i][1] *= Nud.scale

			x1 = mesh[i][0]
			y1 = mesh[i][1]

			mesh[i][0] = x1*self.rotation[0] - y1*self.rotation[1]
			mesh[i][1] = y1*self.rotation[0] + x1*self.rotation[1]

			mesh[i][0] += self.pos[0]
			mesh[i][1] += self.pos[1]

		pygame.draw.polygon(window, self.faction.color, mesh)


	def RemoveOrder(self, o):
		if o in self.orders:
			self.orders.remove(o)
		else:
			print("Tried to remove order from Nud that is not in order list.")

	def normalizeRotation(self):
		d = math.sqrt(self.rotation[0] ** 2 + self.rotation[1] ** 2)
		self.rotation = [self.rotation[0] / d, self.rotation[1] / d]


	#Diplomat AI commands
	
	def command(self, orderType):
		o = Order()
		o.setType(orderType)
		self.orders.append(o)


	def command_addPosition(self, x, y, index = 0):
		self.orders[index].positions.append([x, y])

GOTO_TARGET_ROTATION_TOLERANCE = 1.0

class SmartNudAI:
	def UpdateNud(nud):
		if len(nud.orders) > 0:
			Order.Lookup[nud.orders[0].orderType](nud)


	def GOTO(nud: Nud):
		global GOTO_TARGET_ROTATION_TOLERANCE

		if len(nud.orders[0].positions) < 1:
			print("A goto order was given without a position.")
			return
		
		targetPos = nud.orders[0].positions[0]
		targetDistance = numpy.sqrt((nud.pos[0] - targetPos[0]) ** 2 + (nud.pos[1] - targetPos[1]) ** 2)
		targetVector = getAngleVectorToPoint(nud.pos, targetPos)
		differenceAngle = getVectorAngleDifference(nud.rotation, targetVector) * 180 / numpy.pi

		if PointsInRange(nud.pos, targetPos):
			nud.orders.pop(0)
			return
		if differenceAngle < -GOTO_TARGET_ROTATION_TOLERANCE or differenceAngle > GOTO_TARGET_ROTATION_TOLERANCE:
			SmartNudAI.turn_by_reference_angle(nud, differenceAngle)
			return
		SmartNudAI.move_forward(nud, targetDistance)
	
	def move_forward(nud: Nud, distance):
		if distance > nud.speed:
			distance = nud.speed
		
		nud.pos[0] += nud.rotation[0] * distance
		nud.pos[1] += nud.rotation[1] * distance
	

	def turn_left(nud: Nud, degrees: float):
		if degrees > nud.turnSpeed:
			degrees = nud.turnSpeed
		change = getAngleVector(-degrees)
		nud.rotation = [nud.rotation[0]*change[0]-nud.rotation[1]*change[1], nud.rotation[0]*change[1]+nud.rotation[1]*change[0]]
		nud.normalizeRotation()


	def turn_right(nud: Nud, degrees: float):
		if degrees > nud.turnSpeed:
			degrees = nud.turnSpeed
		change = getAngleVector(degrees)
		nud.rotation = [nud.rotation[0]*change[0]-nud.rotation[1]*change[1], nud.rotation[0]*change[1]+nud.rotation[1]*change[0]]
		nud.normalizeRotation()
	

	def turn_by_reference_angle(nud: Nud, angle: float):
		updatedAngle = numpy.clip(angle, -nud.turnSpeed, nud.turnSpeed)
		turningVector = getAngleVector(updatedAngle)
		nud.rotation = [nud.rotation[0]*turningVector[0]-nud.rotation[1]*turningVector[1], nud.rotation[0]*turningVector[1]+nud.rotation[1]*turningVector[0]]
		nud.normalizeRotation()
		


class DumbNudAI:
	pass


Order.Lookup[Order.TYPE_GOTO] = SmartNudAI.GOTO


def PointsInRange(pos1: tuple[float, float], pos2: tuple[float, float], tolerance: float = 0.1):
	return pos1[0] > pos2[0] - tolerance and pos1[0] < pos2[0] + tolerance and pos1[1] > pos2[1] - tolerance and pos1[1] < pos2[1] + tolerance


def getAngleVectorToPoint(originPos: tuple[float, float], targetPos: tuple[float, float]) -> list[float, float]:
	diffX = targetPos[0] - originPos[0]
	diffY = targetPos[1] - originPos[1]
	d = math.sqrt(diffX ** 2 + diffY ** 2)
	if d == 0:
		return [1.0, 0.0]
	return [diffX / d, diffY / d]


def getAngleVector(angle: float) -> list[float, float]:
	return [math.cos(angle*math.pi/180.0), math.sin(angle*math.pi/180.0)]


"""

Moderately understood use of trigonometery to get the angle between two vectors.
ArcTan2 is used to avoid extremely large values associated with Tangent.

"""
def getVectorAngleDifference(vec1: tuple[float, float], vec2: tuple[float, float]) -> float:
	return numpy.arctan2(vec1[0]*vec2[1]-vec1[1]*vec2[0], vec1[0]*vec2[0]+vec1[1]*vec2[1])


def Input():
	global window, running

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False


fac = None

def Start():
	global instance, fac, n, dim

	fac = Faction("Mythria", (0,100,255))

	for i in range(0, 100, 1):
		n = Nud(fac, [random.randint(0, dim[0]), random.randint(0, dim[1])], 0)
		instance.append(n)

		n.command(Order.TYPE_GOTO)
		n.command_addPosition(random.randint(0, dim[0]), random.randint(0, dim[1]))

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
		nud.Render()

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
