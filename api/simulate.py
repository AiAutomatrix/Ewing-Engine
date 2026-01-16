# api/simulate.py

import random
import numpy as np
from flask import Blueprint, request, jsonify
from engine.config import default_config
from dataclasses import asdict
from engine.dependencies import simulation_instance # Use the singleton

# --- Constants ---
MAX_SIMULATIONS = 25000
MIN_SIMULATIONS = 1

simulate_bp = Blueprint("simulate", __name__)

@simulate_bp.route("/", methods=["POST"])
def simulate():
    data = request.get_json()

    home_team_id = data.get("home_team")
    away_team_id = data.get("away_team")
    num_simulations = data.get("num_simulations", default_config.default_num_simulations)
    random_seed = data.get("random_seed")
    
    # Internal flags not exposed in the API for now
    return_distributions = data.get("return_distributions", False)

    if not home_team_id or not away_team_id:
        return jsonify({"error": "Missing team identifiers"}), 400

    # Use the validation logic from the simulation instance
    if home_team_id not in simulation_instance.teams_by_abbr or away_team_id not in simulation_instance.teams_by_abbr:
        return jsonify({"error": "Team not found"}), 404

    if not (MIN_SIMULATIONS <= num_simulations <= MAX_SIMULATIONS):
        return jsonify({"error": f"Number of simulations must be between {MIN_SIMULATIONS} and {MAX_SIMULATIONS}"}), 400

    if random_seed is not None:
        random.seed(random_seed)
        np.random.seed(random_seed)

    # Use the singleton instance to run the simulation
    metrics = simulation_instance.run_simulation_with_config(
        home_team_id=home_team_id, 
        away_team_id=away_team_id, 
        num_simulations=num_simulations, 
        config=default_config,
        return_distributions=return_distributions
    )

    # Format the output
    output = {
        "summary": asdict(metrics),
        "metadata": {
            "num_simulations": num_simulations,
            "random_seed": random_seed,
            "home_team": home_team_id,
            "away_team": away_team_id,
            "model": "HeuristicModel"
        }
    }
    
    # The old API returned the raw distributions in a separate key
    # The new metrics object nests them inside the summary.
    # To maintain the API contract, we will move them.
    if return_distributions:
        output["distributions"] = {
            "score_skewness": output["summary"].pop("score_skewness"),
            "score_kurtosis": output["summary"].pop("score_kurtosis")
        }


    return jsonify(output)
