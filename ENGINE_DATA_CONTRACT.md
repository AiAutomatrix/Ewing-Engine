# ENGINE_DATA_CONTRACT.md

## Engine Data Contract: Canonical Schemas

This document defines the canonical data structures for the core engine objects: `Player`, `Team`, `Game`, and `BoxScore`. These schemas represent the clean, normalized data that the `ewing-engine` operates on.

**Crucially, all NBA-specific naming conventions, casing (e.g., `PLAYER_ID` vs `player_id`), and any other raw data quirks are resolved *before* data is transformed into these engine objects by the `engine/adapters` layer.** The adapters are responsible for translating raw (e.g., `.parquet` file) data into this standardized format.

---

### 1. Player Object Schema

Represents an individual player within the simulation.

| Field Name | Data Type | Description |
| :--------- | :-------- | :---------- |
| `id`         | `int`       | Unique identifier for the player. |
| `name`       | `str`       | Player's full name. |
| `team_id`    | `int`       | The ID of the team the player belongs to. |
| `minutes`    | `float`     | Minutes played in a game (contextual, often from box score). |
| `points`     | `float`     | Points scored (contextual, often from box score). |
| `rebounds`   | `float`     | Total rebounds (contextual, often from box score). |
| `assists`    | `float`     | Assists (contextual, often from box score). |
| `steals`     | `float`     | Steals (contextual, often from box score). |
| `blocks`     | `float`     | Blocks (contextual, often from box score). |
| `fg_pct`     | `float`     | Field goal percentage (contextual, often from box score). |

*Note: Fields like `minutes`, `points`, `rebounds`, etc., when present on the Player object, are typically contextual (e.g., per-game statistics derived from a BoxScore) rather than intrinsic, immutable identity attributes of the player.*

---

### 2. Team Object Schema

Represents a basketball team within the simulation.

| Field Name | Data Type | Description |
| :--------- | :-------- | :---------- |
| `id`         | `int`       | Unique identifier for the team. |
| `name`       | `str`       | Full team name (e.g., "Los Angeles Lakers"). |
| `abbreviation` | `str`       | Team abbreviation (e.g., "LAL"). |
| `pace`       | `float`     | Team's statistical pace. |
| `off_rating` | `float`     | Team's offensive rating. |
| `def_rating` | `float`     | Team's defensive rating. |
| `efg_pct`    | `float`     | Effective field goal percentage. |
| `three_pt_rate`| `float`     | Three-point attempt rate. |
| `ft_rate`    | `float`     | Free throw attempt rate. |
| `gp`         | `int`       | Games played. |
| `w`          | `int`       | Wins. |
| `l`          | `int`       | Losses. |
| `pts`        | `float`     | Total points. |
| `rebounds`   | `float`     | Total rebounds. |
| `assists`    | `float`     | Total assists. |
| `fg_pct`     | `float`     | Field goal percentage. |
| `turnovers`  | `float`     | Total turnovers. |

---

### 3. Game Object Schema

Represents a single game played between two teams.

| Field Name     | Data Type | Description                      |
| :------------- | :-------- | :------------------------------- |
| `id`           | `int`       | Unique identifier for the game.    |
| `date`         | `str`       | Date of the game (YYYY-MM-DD format). |
| `home_team_id` | `int`       | The ID of the home team.         |
| `away_team_id` | `int`       | The ID of the away team.         |
| `scores`       | `str`       | Placeholder for game scores (e.g., "110-105"). |
| `plus_minus`   | `float`     | Plus/Minus differential for the game (contextual). |

---

### 4. BoxScore Object Schema

Represents player-level statistics for a specific game.

| Field Name | Data Type | Description |
| :--------- | :-------- | :---------- |
| `game_id`    | `int`       | The ID of the game the box score belongs to. |
| `team_id`    | `int`       | The ID of the team the player belongs to in this game. |
| `player_id`  | `int`       | The ID of the player the stats belong to. |
| `minutes`    | `str`       | Minutes played in the game (e.g., "32:45"). |
| `pts`        | `int`       | Points scored by the player in the game. |
| `rebounds`   | `int`       | Rebounds by the player in the game. |
| `assists`    | `int`       | Assists by the player in the game. |
| `fg_pct`     | `float`     | Field goal percentage for the player in the game. |
| `plus_minus` | `int`       | Player's plus/minus for the game. |