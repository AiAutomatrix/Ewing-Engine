# api/capabilities.py

from flask import Blueprint, jsonify

capabilities_bp = Blueprint("capabilities_bp", __name__)

@capabilities_bp.route("/capabilities")
def capabilities():
    """Capabilities endpoint to document what the engine can do."""
    return jsonify(
        {
            "modes": [
                "historical_replay",
                "single_game_simulation",
                "monte_carlo_simulation",
            ],
            "supports_calibration": True,
            "stochastic": True,
            "deterministic_replay": True,
        }
    )
