# Phase 7 Team Dependency Audit

This document outlines the findings of a project-wide audit to identify and remove dependencies on mock team data. The goal of this audit is to ensure that the simulation engine and replay tests use a single, authoritative source of team data derived from the ingestion and adapter pipeline.

## Files Referencing Mock Team Data

The following files were found to have references to `TEAM_DATA`, `LEAGUE_AVG_OFF_RATING`, or `data.teams`:

*   `data/teams.py`: This file contains the mock `TEAM_DATA` and `LEAGUE_AVG_OFF_RATING` definitions. It will be isolated and no longer used by the simulation engine.
*   `tests/test_simulation.py`: This test file imports `TEAM_DATA` and `LEAGUE_AVG_OFF_RATING` from `data/teams.py`. These dependencies will be removed, and the tests will be updated to use ingested data.
*   `api/simulate.py`: The simulation API uses `TEAM_DATA` to initialize teams. This will be refactored to use the team data from the adapters.
*   `engine/sensitivity.py`: The sensitivity analysis module uses `TEAM_DATA`. This will be updated to use the adapted team data.
*   `engine/scenarios.py`: The scenarios module uses `TEAM_DATA`. This will be updated to use the adapted team data.
*   `engine/historical.py`: The historical module uses `TEAM_DATA`. This will be updated to use the adapted team data.

## Plan for Remediation

The following steps will be taken to remove the identified mock data dependencies:

1.  **Isolate `data/teams.py`**: The `data/teams.py` file will be removed from the simulation and replay test execution paths. It may be kept for isolated unit tests or documentation examples.
2.  **Update `tests/test_simulation.py`**: The `tests/test_simulation.py` file will be updated to use team data from the `TeamAdapter`, and the `LEAGUE_AVG_OFF_RATING` will be calculated dynamically.
3.  **Refactor `api/simulate.py`**: The `api/simulate.py` file will be refactored to accept team data from the adapters instead of using the mock `TEAM_DATA`.
4.  **Update `engine/sensitivity.py`**: The `engine/sensitivity.py` module will be updated to accept team data from the adapters.
5.  **Update `engine/scenarios.py`**: The `engine/scenarios.py` module will be updated to accept team data from the adapters.
6.  **Update `engine/historical.py`**: The `engine/historical.py` module will be updated to accept team data from the adapters.

By following these steps, we will ensure that the simulation engine and replay tests use a single, consistent source of team data, which will resolve the test failures and pave the way for future development.
