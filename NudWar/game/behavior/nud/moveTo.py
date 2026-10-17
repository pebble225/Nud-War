from typing import TYPE_CHECKING

from NudWar.game.behavior.nud.action import Action
from NudWar.utils.pumpy import *

import numpy as np

if TYPE_CHECKING:
	from NudWar.game.nuds.nud import Nud

class MoveTo(Action):
	def __init__(self, pos: tuple[float, float], parentAction: Action | None = None, speed: float | None = None):
		"""
		@param pos [x: float, y: float]
		@param speed Measured in meters/tick.
		"""

		super().__init__(parentAction)
		self.pos = pos

		self.speed = speed # meters / tick