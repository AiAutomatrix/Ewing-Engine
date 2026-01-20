# Phase 11 – Test Audit Report

## Environment
- Python version: 3.11.10
- Pytest version: 9.0.2
- Virtualenv active: Yes

## Test Inventory
- test_calibration.py
- test_engine_authority.py
- test_engine_boot.py
- test_full_season_engine_replay.py
- test_monte_carlo_sanity.py
- test_replay_vs_simulation_divergence.py
- test_simulation_bootstrap.py
- test_simulation_config_effects.py
- test_simulation_runner_single_game.py
- test_single_game_engine_replay.py

## Test Results

### ✅ Passed Tests
- tests/test_engine_authority.py::test_engine_authority_ingest_game_failure
- tests/test_engine_boot.py::test_engine_boot
- tests/test_full_season_engine_replay.py::test_full_season_engine_replay
- tests/test_monte_carlo_sanity.py::test_monte_carlo_sanity
- tests/test_simulation_bootstrap.py::test_simulation_bootstrap
- tests/test_simulation_config_effects.py::test_home_court_advantage_effect
- tests/test_simulation_runner_single_game.py::test_simulation_runner_single_game
- tests/test_single_game_engine_replay.py::test_single_game_engine_replay

### ❌ Failed Tests

#### tests/test_calibration.py::test_calibration_parameters_affect_simulation
**Error Type:** AssertionError
**Traceback:**
```text
    def test_calibration_parameters_affect_simulation():
        # Create dummy data
        teams = [
            Team(id=1, name="Team A", abbreviation="A", pace=100, off_rating=110, def_rating=105, efg_pct=0.5, three_pt_rate=0.4, ft_rate=0.2),
            Team(id=2, name="Team B", abbreviation="B", pace=100, off_rating=105, def_rating=110, efg_pct=0.5, three_pt_rate=0.4, ft_rate=0.2),
        ]
        games = []
        boxscores = []
        players = []

        # --- Run with default config (no calibration) ---
        sim_no_calibration = Simulation(players, teams, games, boxscores, config=SimulationConfig(seed=42))
        analysis_no_calibration = sim_no_calibration.run_simulation_with_config(home_team_id="A", away_team_id="B", num_simulations=1)

        # --- Run with calibration that favors home team ---
        calibration_params = CalibrationParams(
            home_offense_scalar=1.2,
            away_offense_scalar=0.8,
            global_score_multiplier=1.1
        )
        config_calibrated = SimulationConfig(seed=42, calibration=calibration_params)
        sim_calibrated = Simulation(players, teams, games, boxscores, config=config_calibrated)
        analysis_calibrated = sim_calibrated.run_simulation_with_config(home_team_id="A", away_team_id="B", num_simulations=1)

        # --- Assertions ---
        # Expect calibrated home score to be higher
>       assert analysis_calibrated.expected_scores['home'] > analysis_no_calibration.expected_scores['home']
E       assert np.float64(71.0) > np.float64(71.0)

tests/test_calibration.py:33: AssertionError
```
**Observed Behavior:**
The test failed because the calibrated simulation's home score was not greater than the non-calibrated simulation's home score. Both resulted in a score of 71.0.

---

#### tests/test_replay_vs_simulation_divergence.py::test_replay_vs_simulation_divergence
**Error Type:** AttributeError
**Traceback:**
```text
    def test_replay_vs_simulation_divergence():
        game_id = '0022300061' # A known good game_id
        print(f"\n--- Running Replay vs Simulation Divergence Test for Game ID: {game_id} ---")

        try:
            # 1. Initialize the global simulation instance
            simulation_instance = get_simulation_instance()

            # 2. Instantiate the Engine
            engine = Engine(simulation_instance=simulation_instance)

            # 3. Ingest the specific game to get its ReplayState (and team abbreviations)
            replay_state = engine.ingest_game(game_id)
            if not replay_state:
                print(f"Error: Could not ingest game {game_id}.")
                sys.exit(1)

            # Fetch team abbreviations from replay_state
            home_team_abbr = replay_state.teams[replay_state.game.home_team].abbreviation
            away_team_abbr = replay_state.teams[replay_state.game.away_team].abbreviation

            # --- Run Deterministic Replay (should match historical box score exactly) ---
            print("\n--- Running Deterministic Historical Replay ---")
            # For direct historical box score comparison, we use run_single_historical_replay
            # which uses the stored actual game_scores
>           replay_result = simulation_instance.run_single_historical_replay(game_id)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: 'Simulation' object has no attribute 'run_single_historical_replay'

tests/test_replay_vs_simulation_divergence.py:31: AttributeError
```
**Observed Behavior:**
The test failed because the `Simulation` object does not have the attribute `run_single_historical_replay`.

---

#### tests/test_simulation_config_effects.py::test_pace_modifier_effect
**Error Type:** AssertionError
**Traceback:**
```text
    def test_pace_modifier_effect():
        """
        Tests that increasing the pace_modifier config param correctly
        increases the total points scored in the game.
        """
        print("\n--- Running Pace Modifier Effect Test ---")
        game_id = '0022300061'
        simulation_instance = get_simulation_instance(force_reload=True)
        target_game = next((g for g in simulation_instance.games if g.id == game_id), None)
        if not target_game:
            raise ValueError(f"Game ID {game_id} not found in loaded games.")

        home_team_abbr = simulation_instance.teams_by_id[target_game.home_team].abbreviation
        away_team_abbr = simulation_instance.teams_by_id[target_game.away_team].abbreviation
        print(f"Testing game: {home_team_abbr} vs {away_team_abbr}")

        # 1. Run a baseline simulation
        print("--- Running Baseline Simulation ---")
        baseline_config = SimulationConfig(seed=42, default_num_simulations=500)
        baseline_result = simulation_instance.run_simulation_with_config(
            home_team_id=home_team_abbr, away_team_id=away_team_abbr, config=baseline_config
        )
        baseline_total_score = baseline_result.expected_scores['home'] + baseline_result.expected_scores['away']
        print(f"Baseline Avg Total Score: {baseline_total_score:.2f}")

        # 2. Run a modified simulation with an increased pace modifier
        print("--- Running Modified Simulation (Increased Pace) ---")
        modified_config = SimulationConfig(seed=42, default_num_simulations=500, pace_modifier=1.2)
        modified_result = simulation_instance.run_simulation_with_config(
            home_team_id=home_team_abbr, away_team_id=away_team_abbr, config=modified_config
        )
        modified_total_score = modified_result.expected_scores['home'] + modified_result.expected_scores['away']
        print(f"Modified Avg Total Score: {modified_total_score:.2f}")

        # 3. Assert divergence
>       assert modified_total_score > baseline_total_score
E       assert np.float64(134.742) > np.float64(134.742)

tests/test_simulation_config_effects.py:87: AssertionError
```
**Observed Behavior:**
The test failed because the modified simulation with an increased pace modifier did not result in a higher total score. Both the baseline and modified simulations produced an average total score of 134.74.

---

## Summary

Total tests run: 11
Passed: 8
Failed: 3
Deterministic failures observed: Yes
Engine import failures: No
API startup blockers: No

## Notes
The same random seed (42) was used in the failing `test_calibration_parameters_affect_simulation` and `test_pace_modifier_effect` tests, which could be a factor in the deterministic failures.
