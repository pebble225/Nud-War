import pygame
import math
import numpy

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
		self.speed = 10
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

	#Nud AI commands
	
	def move_forward(self, distance):
		if distance > self.speed:
			distance = self.speed
		
		self.pos[0] += self.rotation[0] * distance
		self.pos[1] += self.rotation[1] * distance
	

	def turn_left(self, degrees):
		if degrees > self.turnSpeed:
			degrees = self.turnSpeed
		change = getAngleVector(-degrees)
		self.rotation = [self.rotation[0]*change[0]-self.rotation[1]*change[1], self.rotation[0]*change[1]+self.rotation[1]*change[0]]
		self.normalizeRotation()


	def turn_right(self, degrees):
		if degrees > self.turnSpeed:
			degrees = self.turnSpeed
		change = getAngleVector(degrees)
		self.rotation = [self.rotation[0]*change[0]-self.rotation[1]*change[1], self.rotation[0]*change[1]+self.rotation[1]*change[0]]
		self.normalizeRotation()


	#Diplomat AI commands
	
	def command(self, orderType):
		o = Order()
		o.setType(orderType)
		self.orders.append(o)


	def command_addPosition(self, x, y, index = 0):
		self.orders[index].positions.append([x, y])

class SmartNudAI:
	def UpdateNud(nud):
		if len(nud.orders) > 0:
			Order.Lookup[nud.orders[0].orderType](nud)


	def GOTO(nud):
		GOTO_TARGET_RANGE = 2

		if len(nud.orders[0].positions) < 1:
			print("A goto order was given without a position.")
			return
		
		targetPos = nud.orders[0].positions[0]

		
		


class DumbNudAI:
	pass


Order.Lookup[Order.TYPE_GOTO] = SmartNudAI.GOTO


def PointsInRange(pos1, pos2, tolerance, d = -1):
	if d == -1:
		d = math.sqrt((pos2[0]-pos1[0])*(pos2[0]-pos1[0]) + (pos2[1]-pos1[1])*(pos2[1]-pos1[1]))
	#floating points maaaan
	return d < tolerance


def getAngleToPoint(origin: tuple[float, float], target: tuple[float, float], d = -1):
	if d == -1:
		d = math.sqrt((target[0]-origin[0])*(target[0]-origin[0]) + (target[1]-origin[1])*(target[1]-origin[1]))
	diff = target[1] - origin[1]
	return (math.asin(diff / d)*180 / math.pi) % 360


def getTargetAngleIsCloserClockwise(r, targetAngle):
	if r > targetAngle:
		return r - targetAngle > 180.0
	else:
		return targetAngle - r < 180.0


def getAngleVector(angle: float) -> list[float, float]:
	return [math.cos(angle*math.pi/180.0), math.sin(angle*math.pi/180.0)]


def Input():
	global window, running

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False


fac = None
n = None

def Start():
	global instance, fac, n

	fac = Faction("Mythria", (0,100,255))

	n = Nud(fac, [100, 100], 0)

	n.command(Order.TYPE_GOTO)
	n.command_addPosition(800, 400)

def Update():
	global instance, n

	#step 1: Run spatial abstract to update nud math (might not need this step)

	#step 2: run the diplomat AI

	#step 3: run the Nud AI and Dumb AI

	SmartNudAI.UpdateNud(n)


def Render():
	global window, instance, fac, n

	window.fill((0, 0, 0))

	n.Render()

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
