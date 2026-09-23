from abc import ABC

class Constants:
	def __init__(self):
		"""
		Includes any global data that can't be directly configured by the user. Also includes unit conversions for easy access.

		This is meant to be reinitialized where needed and should only include independent data. (pure integers, floats, strings)

		@param tickRate (ticks/second). Equivelance between ticks and seconds.
		@param MSPerTick (milliseconds/tick). Gives the length of a tick in milliseconds.
		@param UnitsPerTick (units/tick). Velocity measurement used to convert between units/second. Unit is like a meter.
		"""

		self.tickRate = 60.0
		self.MSPerTick = 1000.0 / self.tickRate
		self.UnitsPerTick = 1.0 / self.tickRate

	def ToUnitsPerTick(self, units: float):
		"""
		Converts from units/second to units/tick. Call this when directly setting the speed of an object.

		@param units (units/second)
		"""
		return units * self.UnitsPerTick

	def ToUnitsPerSecond(self, units: float):
		"""
		Converts from units/tick to units/second.

		@param units (units/tick)
		"""
		return units * self.tickRate