
import numpy as np
from engine.dependencies import get_simulation_instance
from engine.config import SimulationConfig, CalibrationParams
from engine.models import HeuristicModel
from calibration_analysis.metrics import analyze_simulation_results

def run_test_for_parameter(simulation, parameter_name, baseline_value, modified_value):
    """Runs a controlled test for a single calibration parameter."""

    # --- Baseline Run ---
    baseline_params_dict = { p: 1.0 for p in PARAMETER_KEYS if p != 'pace_standard_deviation' }
    baseline_params_dict['pace_standard_deviation'] = 10.0
    baseline_params = CalibrationParams(**baseline_params_dict)
    baseline_config = SimulationConfig(calibration=baseline_params, seed=42) # Seed for reproducibility
    baseline_model_kwargs = {'league_avg_off_rating': simulation.league_avg_off_rating, 'calibration': baseline_params}
    baseline_model = HeuristicModel(**baseline_model_kwargs)
    
    baseline_results = [
        simulation.simulate_game(baseline_model, "GSW", "LAL", baseline_config) 
        for _ in range(500)
    ]
    baseline_metrics = analyze_simulation_results(baseline_results)

    # --- Modified Run ---
    modified_params_dict = baseline_params_dict.copy()
    modified_params_dict[parameter_name] = modified_value
    modified_params = CalibrationParams(**modified_params_dict)
    modified_config = SimulationConfig(calibration=modified_params, seed=42)
    modified_model_kwargs = {'league_avg_off_rating': simulation.league_avg_off_rating, 'calibration': modified_params}
    modified_model = HeuristicModel(**modified_model_kwargs)

    modified_results = [
        simulation.simulate_game(modified_model, "GSW", "LAL", modified_config) 
        for _ in range(500)
    ]
    modified_metrics = analyze_simulation_results(modified_results)

    # --- Output ---
    print(f"Parameter: {parameter_name}")
    print("Baseline Metrics:")
    print(f"  avg_points: {baseline_metrics['average_total_points']:.4f}")
    print(f"  home_win_rate: {baseline_metrics['home_win_rate']:.4f}")
    print(f"  mov_stddev: {baseline_metrics['margin_of_victory_stddev']:.4f}")

    print("\nModified Metrics:")
    print(f"  avg_points: {modified_metrics['average_total_points']:.4f}")
    print(f"  home_win_rate: {modified_metrics['home_win_rate']:.4f}")
    print(f"  mov_stddev: {modified_metrics['margin_of_victory_stddev']:.4f}")

    print("\nObserved Effect:")
    for metric in sorted(baseline_metrics.keys()):
        diff = modified_metrics[metric] - baseline_metrics[metric]
        if abs(diff) < 1e-4:
            effect = "none"
        elif diff > 0:
            effect = "↑"
        else:
            effect = "↓"
        print(f"  {metric.replace('_', ' ')}: {effect}")

    # --- Conclusion ---
    is_effective = any(abs(modified_metrics[m] - baseline_metrics[m]) > 1e-4 for m in baseline_metrics)
    conclusion = "EFFECTIVE" if is_effective else "NO-OP"
    print(f"\nConclusion: {conclusion}")
    print("-" * 30)


PARAMETER_KEYS = [
    'global_score_multiplier',
    'pace_modifier',
    'pace_standard_deviation',
    'home_offense_scalar',
    'home_defense_scalar',
    'away_offense_scalar',
    'away_defense_scalar'
]

PARAMETER_DELTAS = {
    "global_score_multiplier": 1.3,
    "pace_modifier": 1.1,
    "pace_standard_deviation": 20.0,
    "home_offense_scalar": 1.1,
    "home_defense_scalar": 0.9,
    "away_offense_scalar": 1.1,
    "away_defense_scalar": 0.9,
}

def main():
    print("=== Calibration Parameter Verification ===")
    simulation = get_simulation_instance(force_reload=True)
    
    for param, modified_value in PARAMETER_DELTAS.items():
        baseline_value = 10.0 if param == 'pace_standard_deviation' else 1.0
        run_test_for_parameter(simulation, param, baseline_value, modified_value)

if __name__ == "__main__":
    main()
