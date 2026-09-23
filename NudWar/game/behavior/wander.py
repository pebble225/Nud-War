from abc import ABC, abstractmethod

from NudWar.game.behavior.action import Action

class Wander(Action):
	def __init__(self):
		super().__init__()

	def Update(self) -> int:
		# bring a timer here
		return Action.RUNNING