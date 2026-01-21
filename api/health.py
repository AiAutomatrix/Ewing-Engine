# api/health.py

from flask import Blueprint, jsonify
from engine.dependencies import get_simulation_instance

health_bp = Blueprint("health_bp", __name__)

@health_bp.route("/health")
def health():
    """Health endpoint to confirm the engine is loaded."""
    sim = get_simulation_instance()
    return jsonify(
        {
            "engine_loaded": sim is not None,
            "teams": len(sim.teams),
            "games": len(sim.games),
            "boxscores": len(sim.boxscores),
        }
    )
