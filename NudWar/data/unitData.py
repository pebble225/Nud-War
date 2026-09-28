from abc import ABC

class UnitData:
	def __init__(self):
		self.tickRate = 60.0
		self.MSPerTick = 1000.0 / self.tickRate
		self.MetersPerTick = 1.0 / self.tickRate

		self.NUD_IDLETIME_MIN = 2.0
		self.NUD_IDLETIME_MAX = 8.0

	def ToMetersPerTick(self, meters: float):
		"""
		Converts from meters/second to meters/tick. Call this when directly setting the speed of an object.

		@param units (units/second)
		"""
		return meters * self.MetersPerTick

	def ToDegreesPerTick(self, degrees: float):
		return self.ToMetersPerTick(degrees)

	def ToMetersPerSecond(self, meters: float):
		"""
		Converts from units/tick to units/second.

		@param units (units/tick)
		"""
		return meters * self.tickRate

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
	constants = UnitData()