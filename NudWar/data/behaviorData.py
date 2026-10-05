class BehaviorData:
	def __init__(self):

		self.TELEPORT_WAIT_COST = 2 # seconds
		"""
		The time a nud needs to wait at a portal before they start teleporting
		"""

		self.STANDARD_DISTANCE_TOLERANCE = 1 # meters
		"""
		Used when checking if objects are considered close enough to one another.
		"""

		self.WANDER_SMALL_STEP_DISTANCE = 5 # meters
		"""
		During wandering, nuds will occassionally take small steps of this max length instead of random positions.
		"""