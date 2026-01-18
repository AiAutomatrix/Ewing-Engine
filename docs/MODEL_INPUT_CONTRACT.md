# MODEL_INPUT_CONTRACT.md

This document defines the contract for feature vectors intended for consumption by machine learning models or for advanced simulation tuning. It specifies the expected structure, temporal context, and potential target variables derived from the engine's `ReplayState` and feature extraction process.

## 1. Overall Shape of the Feature Vector

The primary feature vector for a model will be a flat, numerical representation of a single game instance at the point of prediction (e.g., pre-game for outcome prediction, or end-of-quarter for in-game predictions).

*   **Format:** Typically a flat vector (or a row in a DataFrame) where each column represents a specific feature.
*   **Granularity:** Per-game (or per-possession for more granular models, if features support that).
*   **Structure:** Concatenation of game-level, home team-level, away team-level, and potentially relevant player-level features.

**Example Structure (Conceptual):**

```
[
    game_features...,
    home_team_features...,
    away_team_features...,
    player_features_home_star_1...,
    player_features_away_star_1...,
    ...
]
```
## 2. Temporal Framing

Features will be framed to represent the state of the game *before* the event being predicted.

*   **Per-Game (Primary):** Features describing the two teams and game context *prior* to the game start. This is the current focus.
*   **Rolling Window (Future):** Aggregated player/team statistics over the last N games.
*   **Season-to-Date (Future):** Aggregated player/team statistics from the start of the season up to the current game.

For the immediate future, all features derived from `ReplayState` will implicitly represent the state **at the time of the game's completion for historical replays**, but conceptually they should reflect information available *before* the game or event to avoid data leakage for predictive models.

## 3. Target Variables (Definitions - Not Computed Yet)

This section defines potential target variables that models might predict, derived from the actual game outcomes (box scores).

*   **`home_team_win`**: Binary (1 if home team wins, 0 otherwise).
    *   *Source:* `game__home_score_actual` vs `game__away_score_actual`.
*   **`home_team_score_margin`**: Integer (home team actual score - away team actual score).
    *   *Source:* `game__home_score_actual` and `game__away_score_actual`.
*   **`total_points`**: Integer (home team actual score + away team actual score).
    *   *Source:* `game__home_score_actual` and `game__away_score_actual`.
*   **`player_performance_metric_<ID>`**: Numerical (e.g., a player's actual points, rebounds, assists in the game).
    *   *Source:* `player__<ID>__player_points_in_game`, etc., from `FEATURE_REGISTRY.md`.

## 4. Reference to Feature Definitions

Detailed definitions, origins, and preliminary audit statistics for individual features can be found in:

*   [`FEATURE_REGISTRY.md`](./FEATURE_REGISTRY.md)

This contract ensures consistency and clarity when developing and evaluating models using the features extracted by the engine.