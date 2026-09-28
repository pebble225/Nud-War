from abc import ABC, abstractmethod

import uuid

class GameObject(ABC):
	def __init__(self):
		self.id = uuid.uuid1()

	def GetID(self) -> uuid.UUID:
		return self.id