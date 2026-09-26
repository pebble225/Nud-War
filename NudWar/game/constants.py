from abc import ABC

class Constants:
	def __init__(self):
		"""
		Includes any global data that can't be directly configured by the user. Also includes unit conversions for easy access.

		This is meant to be reinitialized where needed and should only include independent data. (pure integers, floats, strings)

		@param tickRate (ticks/second). Equivelance between ticks and seconds.
		@param MSPerTick (milliseconds/tick). Gives the length of a tick in milliseconds.
		@param MetersPerTick (units/tick). Velocity measurement used to convert between units/second.
		"""

		self.tickRate = 60.0
		self.MSPerTick = 1000.0 / self.tickRate
		self.MetersPerTick = 1.0 / self.tickRate

		self.NUD_IDLETIME_MIN = 2.0
		self.NUD_IDLETIME_MAX = 8.0

	def ToMetersPerTick(self, units: float):
		"""
		Converts from meters/second to meters/tick. Call this when directly setting the speed of an object.

		@param units (units/second)
		"""
		return units * self.MetersPerTick

	def ToMetersPerSecond(self, units: float):
		"""
		Converts from units/tick to units/second.

		@param units (units/tick)
		"""
		return units * self.tickRate

	def ToTicks(self, time: int):
		"""
		Converts from seconds to ticks.
		"""
		return time * self.tickRate

	def ToSeconds(self, time: int):
		"""
		Converts from ticks to seconds.
		"""
		return time / self.tickRate

if __name__ == "__main__":
	constants = Constants()