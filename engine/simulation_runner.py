import os
from engine.simulation import Simulation
from engine.config import SimulationConfig, default_config

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

def run_single_game_simulation(simulation_instance: Simulation, home_team_abbr: str, away_team_abbr: str, num_simulations: int = None, config: SimulationConfig = None):
    """
    Runs a single game simulation with the given parameters and returns the simulation analysis.
    """
    if config is None:
        config = default_config

    return simulation_instance.run_simulation_with_config(
        home_team_id=home_team_abbr,
        away_team_id=away_team_abbr,
        num_simulations=num_simulations,
        config=config
    )