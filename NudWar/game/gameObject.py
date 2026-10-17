from abc import ABC, abstractmethod
import weakref
import uuid

class GameObject(ABC):
	def __init__(self):
		self.id = uuid.uuid1()

	def GetID(self) -> uuid.UUID:
		return weakref.ref(self.id)