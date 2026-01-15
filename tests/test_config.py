# tests/test_config.py

from engine.config import SimulationConfig, default_config

def test_default_config_values():
    """Tests that the default configuration loads with expected values."""
    assert default_config.avg_pace == 100.0
    assert default_config.home_court_advantage == 2.0
    assert default_config.default_num_simulations == 1000

def test_config_override():
    """Tests that the SimulationConfig can be overridden."""
    custom_config = SimulationConfig(avg_pace=110.0, default_num_simulations=500)
    assert custom_config.avg_pace == 110.0
    assert custom_config.default_num_simulations == 500
