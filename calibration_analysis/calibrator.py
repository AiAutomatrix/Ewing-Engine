# calibration_analysis/calibrator.py

import json
import os
from typing import Dict, Any, List

from engine.simulation import Simulation
from engine.config import SimulationConfig
from engine.calibration import CalibrationParams
from engine.metrics import SimulationMetrics
from .metrics import analyze_simulation_results, compare_to_targets

class Calibrator:
    """
    Orchestrates the simulation calibration process.

    This class manages running simulations with different parameters, analyzing
    the outputs against historical targets, and generating reports to document
    the calibration process and its impact.
    """
    def __init__(self, simulation_instance: Simulation, base_report_dir: str = "calibration/reports"):
        self.simulation_instance = simulation_instance
        self.base_report_dir = base_report_dir
        os.makedirs(self.base_report_dir, exist_ok=True)

    def _reconstruct_results_from_metrics(self, metrics: SimulationMetrics) -> List[Dict[str, Any]]:
        """
        Reconstructs a list of individual game result dictionaries from a
        SimulationMetrics object.
        """
        home_scores = metrics.score_distributions['home']
        away_scores = metrics.score_distributions['away']
        
        reconstructed_results = []
        for hs, as_ in zip(home_scores, away_scores):
            reconstructed_results.append({
                "home_score": hs,
                "away_score": as_,
                "total_points": hs + as_,
                "winner": "home" if hs > as_ else "away",
            })
        return reconstructed_results

    def run_baseline_snapshot(self, matchups: List[Dict[str, str]], num_simulations: int = 1000) -> Dict[str, Any]:
        """
        Runs a baseline simulation snapshot with default parameters and saves the results.
        """
        print("Running baseline snapshot...")
        
        baseline_config = SimulationConfig(calibration=CalibrationParams())

        all_results = []
        for matchup in matchups:
            metrics_object = self.simulation_instance.run_simulation_with_config(
                home_team_id=matchup["home"],
                away_team_id=matchup["away"],
                num_simulations=num_simulations,
                config=baseline_config,
                return_distributions=True
            )
            reconstructed = self._reconstruct_results_from_metrics(metrics_object)
            all_results.extend(reconstructed)

        analysis = analyze_simulation_results(all_results)
        comparison = compare_to_targets(analysis)
        
        self._generate_report(step_name="baseline", params={}, comparison_metrics=comparison)
        
        print("Baseline snapshot complete.")
        return comparison

    def run_and_report_single_config(self, params: CalibrationParams, matchups: List[Dict[str, str]], num_simulations: int, report_name: str) -> None:
        """
        Runs a simulation with a single, specific configuration and generates a report.
        """
        print(f"Running single configuration: {report_name}")
        config = SimulationConfig(calibration=params)

        all_results = []
        for matchup in matchups:
            metrics_object = self.simulation_instance.run_simulation_with_config(
                home_team_id=matchup["home"],
                away_team_id=matchup["away"],
                num_simulations=num_simulations,
                config=config,
                return_distributions=True
            )
            reconstructed = self._reconstruct_results_from_metrics(metrics_object)
            all_results.extend(reconstructed)

        analysis = analyze_simulation_results(all_results)
        comparison = compare_to_targets(analysis)
        
        param_dict = {
            "global_score_multiplier": params.global_score_multiplier,
            "pace_modifier": params.pace_modifier,
            "pace_standard_deviation": params.pace_standard_deviation
        }
        
        self._generate_report(step_name=report_name, params=param_dict, comparison_metrics=comparison)
        print(f"Finished single configuration: {report_name}")

    def run_single_parameter_calibration(
        self, 
        parameter_name: str, 
        values: List[float], 
        matchups: List[Dict[str, str]], 
        num_simulations: int = 1000
    ) -> None:
        """
        Runs a calibration step for a single parameter across a range of values.
        """
        print(f"Running calibration for parameter: {parameter_name}")

        for i, value in enumerate(values):
            step_name = f"{parameter_name}_step_{i}"
            print(f"  - Running {step_name} with value: {value}")

            params = {parameter_name: value}
            calibration_params = CalibrationParams(**params)
            config = SimulationConfig(calibration=calibration_params)

            all_results = []
            for matchup in matchups:
                metrics_object = self.simulation_instance.run_simulation_with_config(
                    home_team_id=matchup["home"],
                    away_team_id=matchup["away"],
                    num_simulations=num_simulations,
                    config=config,
                    return_distributions=True
                )
                reconstructed = self._reconstruct_results_from_metrics(metrics_object)
                all_results.extend(reconstructed)

            analysis = analyze_simulation_results(all_results)
            comparison = compare_to_targets(analysis)
            
            self._generate_report(step_name=step_name, params=params, comparison_metrics=comparison)

        print(f"Calibration for {parameter_name} complete.")

    def _generate_report(self, step_name: str, params: Dict[str, Any], comparison_metrics: Dict[str, Any]) -> None:
        """
        Generates a markdown report for a calibration step.
        """
        report_path = os.path.join(self.base_report_dir, f"{step_name}.md")
        
        content = f"# Calibration Report: {step_name}\n\n"
        content += f"**Parameters Used:**\n```json\n{json.dumps(params, indent=2)}\n```\n\n"
        content += "**Metrics vs. Targets:**\n\n"
        content += "| Metric | Simulated | Target | Error | Tolerance |\n"
        content += "|---|---|---|---|---|\n"
        
        for metric, values in comparison_metrics.items():
            content += f"| {metric} | {values['simulated']:.4f} | {values['target']:.4f} | {values['error']:.4f} | {values['tolerance']:.4f} |\n"
            
        with open(report_path, "w") as f:
            f.write(content)
        print(f"Report generated: {report_path}")
