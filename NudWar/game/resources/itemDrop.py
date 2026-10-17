from NudWar.game.transformGameObject import TransformGameObject

from NudWar.game.resources.resourceDefinition import ResourceDefinition

class ItemDrop(TransformGameObject):
	def __init__(self, resourceType: ResourceDefinition):
		super().__init__()

		self.resourceType: ResourceDefinition = resourceType