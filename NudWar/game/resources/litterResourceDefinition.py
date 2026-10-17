from NudWar.game.resources.resourceDefinition import ResourceDefinition

class LitterResourceDefinition(ResourceDefinition):
	def __init__(self, name):
		"""
		A litter resource is obtained by finding it on the ground and picking it up.
		"""
		super().__init__(name)