# engine/possessions.py

import random
from .models import SimulationModel

def get_possession_outcome(model: SimulationModel, off_team, def_team) -> int:
    """
    Wrapper to get possession outcome from the provided model.
    This abstraction allows for future enhancements, like possession-level modifiers.
    """
    return model.get_possession_outcome(off_team, def_team)
