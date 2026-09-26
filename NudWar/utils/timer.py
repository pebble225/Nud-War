class Timer:
	def __init__(self, currentTime: int, duration: int):
		self.startTime = currentTime
		self.endTime = currentTime + duration

	def IsCompleted(self, gameTime: int):
		return gameTime >= self.endTime