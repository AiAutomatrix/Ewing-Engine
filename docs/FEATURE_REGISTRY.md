# Feature Registry and Lineage

This document defines the features extracted by the `ewing-engine` for each game replay. These features are extracted from the `ReplayState` after the game data has been ingested and are intended for use in downstream modeling and analysis. All features represent values pertaining to a single game instance after it has been processed by the engine.

## Core Principles

*   **Source of Truth:** All features are derived from the original `games.parquet` and `boxscores.parquet` data, transformed into engine objects (`Game`, `Team`, `Player`, `BoxScore`).
*   **Replay-Centric:** Features are calculated *per game replay*, reflecting the state and outcomes within that specific game context.
*   **Clarity & Traceability:** Each feature's definition includes its source within the `ReplayState` and any transformations applied.

---

## 1. Game-Level Features

These features describe characteristics of the game itself.

| Feature Name          | Data Type | Source / Calculation                                                | Description                                       |
| :-------------------- | :-------- | :------------------------------------------------------------------ | :------------------------------------------------ |
| `game__game_id`       | `str`     | `ReplayState.game.id`                                               | Unique identifier for the game.                   |
| `game__game_date`     | `str`     | `ReplayState.game.date`                                             | Date of the game (YYYY-MM-DD format).             |
| `game__home_team_id`  | `int`     | `ReplayState.game.home_team`                                        | Numeric ID of the home team.                      |
| `game__away_team_id`  | `int`     | `ReplayState.game.away_team`                                        | Numeric ID of the away team.                      |
| `game__home_team_abbr`| `str`     | `ReplayState.teams[home_team_id].abbreviation`                      | Abbreviation of the home team.                    |
| `game__away_team_abbr`| `str`     | `ReplayState.teams[away_team_id].abbreviation`                      | Abbreviation of the away team.                    |
| `game__home_score_actual` | `int`   | Sum of `BoxScore.pts` for all players on `home_team_id` in `ReplayState.boxscores` | Actual points scored by the home team. |
| `game__away_score_actual` | `int`   | Sum of `BoxScore.pts` for all players on `away_team_id` in `ReplayState.boxscores` | Actual points scored by the away team. |

---

## 2. Team-Level Features (Per Team in Game)

These features describe characteristics of each team participating in a specific game. Each game will produce two sets of these features, one for the home team and one for the away team, identifiable by their respective team IDs.

| Feature Name                      | Data Type | Source / Calculation                                                | Description                                                       |
| :-------------------------------- | :-------- | :------------------------------------------------------------------ | :---------------------------------------------------------------- |
| `team__<ID>__team_id`             | `int`     | `ReplayState.teams[ID].id`                                          | Unique identifier for the team.                                   |
| `team__<ID>__team_name`           | `str`     | `ReplayState.teams[ID].name`                                        | Full name of the team.                                            |
| `team__<ID>__team_abbreviation`   | `str`     | `ReplayState.teams[ID].abbreviation`                               | Team abbreviation.                                                |
| `team__<ID>__team_score_in_game`  | `int`     | Sum of `BoxScore.pts` for players on this team in `ReplayState.boxscores` | Total points scored by this team in the game.                  |
| `team__<ID>__team_pace_season_avg`| `float`   | `ReplayState.teams[ID].pace`                                       | Season average pace for the team (placeholder, currently 0.0 in initial `Team` object). |
| `team__<ID>__team_off_rating_season_avg` | `float` | `ReplayState.teams[ID].off_rating`                                 | Season average offensive rating for the team (placeholder, currently 0.0). |
| `team__<ID>__team_def_rating_season_avg` | `float` | `ReplayState.teams[ID].def_rating`                                 | Season average defensive rating for the team (placeholder, currently 0.0). |

*Note: `<ID>` is a placeholder for the actual team ID (e.g., `team__1610612737__team_id`).*

---

## 3. Player-Level Features (Per Player in Game)

These features describe characteristics and performance of each player who participated in a specific game.

| Feature Name                       | Data Type | Source / Calculation                                                | Description                                                       |
| :--------------------------------- | :-------- | :------------------------------------------------------------------ | :---------------------------------------------------------------- |
| `player__<ID>__player_id`          | `int`     | `ReplayState.players[ID].id`                                        | Unique identifier for the player.                                 |
| `player__<ID>__player_name`        | `str`     | `ReplayState.players[ID].name`                                      | Player's full name.                                               |
| `player__<ID>__player_team_id_in_game` | `int`   | `BoxScore.team_id` for this player in this game                     | The ID of the team the player played for in this specific game. |
| `player__<ID>__player_minutes_in_game` | `float` | `BoxScore.minutes` for this player in this game                     | Minutes played by this player in this specific game.             |
| `player__<ID>__player_points_in_game` | `float` | `BoxScore.pts` for this player in this game                         | Points scored by this player in this specific game.              |
| `player__<ID>__player_rebounds_in_game` | `float` | `BoxScore.rebounds` for this player in this game                    | Total rebounds by this player in this specific game.             |
| `player__<ID>__player_assists_in_game` | `float` | `BoxScore.assists` for this player in this game                     | Assists by this player in this specific game.                    |
| `player__<ID>__player_fg_pct_in_game` | `float` | `BoxScore.fg_pct` for this player in this game                      | Field goal percentage for this player in this specific game.     |

*Note: `<ID>` is a placeholder for the actual player ID (e.g., `player__1629060__player_id`).*

---

## Conclusion

These features represent the direct, raw statistical output of individual game replays, structured to be easily consumable by machine learning models or for further aggregate analysis. They are the direct result of processing the raw `.parquet` data through the engine's ingestion and feature extraction pipeline, ensuring a consistent and validated data foundation.