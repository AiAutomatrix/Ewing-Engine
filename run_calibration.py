
# run_calibration.py

from engine.dependencies import get_simulation_instance
from calibration_analysis.calibrator import Calibrator
from engine.config import CalibrationParams

def main():
    """
    Main function to execute the calibration process.
    """
    print("Initializing calibration process...")

    # 1. Get the simulation instance
    simulation = get_simulation_instance()

    # 2. Instantiate the Calibrator
    calibrator = Calibrator(simulation_instance=simulation)

    # 3. Define fixed matchups for consistent calibration runs
    matchups = [
        {"home": "GSW", "away": "LAL"},
        {"home": "BKN", "away": "CHA"},
        {"home": "MIL", "away": "PHX"},
        {"home": "UTA", "away": "DEN"},
    ]

    # 4. Run a "best-guess" calibration
    best_guess_params = CalibrationParams(
        global_score_multiplier=1.8,
        pace_modifier=1.05,
        pace_standard_deviation=25.0
    )
    calibrator.run_and_report_single_config(
        params=best_guess_params,
        matchups=matchups,
        num_simulations=1000, # Increased for more accurate results
        report_name="best_guess_run_extreme_variance"
    )

    print("Calibration process finished.")

if __name__ == "__main__":
    main()
