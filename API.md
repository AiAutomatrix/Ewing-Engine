# Ewing-Engine API Documentation

This document provides a detailed overview of the `ewing-engine` API, including all available endpoints, their functionalities, and example `curl` commands for each.

## Base URL

All API endpoints are relative to the following base URL:

```
http://127.0.0.1:5000
```

---

## Endpoints

### 1. Health Check

*   **Endpoint:** `/health`
*   **Method:** `GET`
*   **Description:** Provides a simple health check to confirm that the simulation engine is loaded and running correctly. It returns a JSON object with information about the loaded data.
*   **Example Request:**

    ```bash
    curl http://127.0.0.1:5000/health
    ```

*   **Example Response:**

    ```json
    {
      "boxscores": 32385,
      "engine_loaded": true,
      "games": 1230,
      "teams": 30
    }
    ```

### 2. Game Simulation

*   **Endpoint:** `/simulate/`
*   **Method:** `POST`
*   **Description:** Simulates a basketball game between two teams for a specified number of iterations. It returns a detailed analysis of the simulation results.

*   **Request Body (JSON):**

| Parameter              | Type    | Required | Description                                                                                                                               |
| ---------------------- | ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `home_team`            | String  | Yes      | The three-letter abbreviation for the home team (e.g., "GSW").                                                                          |
| `away_team`            | String  | Yes      | The three-letter abbreviation for the away team (e.g., "LAL").                                                                          |
| `num_simulations`      | Integer | No       | The number of game simulations to run. Must be between 1 and 25,000. Defaults to the value in the simulation configuration.                  |
| `random_seed`          | Integer | No       | A seed for the random number generator to ensure deterministic results. If not provided, the simulation will not be reproducible.         |
| `return_distributions` | Boolean | No       | If `true`, the response will include the raw score distributions. Defaults to `false`.                                                    |


*   **Example Request:**

    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"home_team": "GSW", "away_team": "LAL", "num_simulations": 1000, "random_seed": 42}' \
    http://127.0.0.1:5000/simulate/
    ```

*   **Example Response:**

    The response is a JSON object containing the simulation summary and metadata.

    ```json
    {
      "metadata": {
        "away_team": "LAL",
        "home_team": "GSW",
        "model": "HeuristicModel",
        "num_simulations": 1000,
        "random_seed": 42
      },
      "summary": {
        "expected_margin": 10.51,
        "expected_scores": {
          "away": 107.82,
          "home": 118.33
        },
        "expected_total_points": 226.15,
        // ... other summary statistics
        "win_probability": {
          "away": 0.15,
          "draw": 0.0,
          "home": 0.85
        }
      }
    }
    ```
