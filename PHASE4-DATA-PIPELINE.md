# Phase 4 — NBA Stats API Exploration & Data Pipeline Setup

## Objective
Use the `nba_api` Python package to explore, test, document, and learn the structure of the NBA official stats API. This will generate raw data structures and schema definitions that your engine can later use for simulations and modeling (Phase 5). This phase focuses exclusively on **API exploration, testing, and data schema discovery**.

---

## Requirements

1. Python 3.10+
2. Install the `nba_api` package via pip
3. Explore endpoints, validate responses, and create tests for each endpoint’s data structure
4. Do **not** integrate the data into the engine yet — first we *understand* the data

---

## Step 1 — Install and Verify the Client

### Install `nba_api`
```bash
pip install nba_api
```

### Verify installation
```bash
python - << 'EOF'
import nba_api
print("nba_api installed:", nba_api.__version__)
EOF
```

---

## Step 2 — Identify Core Endpoint Categories

Use the `nba_api.stats.endpoints` module. Each class in this module wraps a Stats API endpoint at:

`https://stats.nba.com/stats/<endpoint>?<params>`

The agent should generate terminal tests to verify calls succeed and that returned data can be read into pandas DataFrames (if pandas is installed).

---

## Step 3 — Core Endpoints to Explore

### League & Static Info
- `commonallplayers` — list all players for seasons
- `commonteamyears` — team roster history
- `leaguegamefinder` — find games meeting filters

### Player Stats
- `playercareerstats` — player career totals and splits
- `playergamelog` — player game-by-game stats
- `playerprofilev2` — detailed player profile
- `leaguedashplayerstats` — league player stats by season
- `leaguedashplayerbiostats` — league player basic stats
- `playerdashboardbygamesplits` — player split stats

### Team Stats
- `leaguedashteamstats` — league team stats by season
- `teamgamefinder` — find games for teams
- `teamplayeronoffdetails` — on/off stats for team players

### Box Score Endpoints
- `boxscoretraditionalv3` — traditional box score per game
- `boxscoreadvancedv3` — advanced box score metrics
- `boxscoreusagev3` — player usage stats
- `boxscorescoringv3` — scoring related stats

### Play-By-Play (Optional)
- `playbyplayv2` — play-by-play for a given game

---

## Step 4 — Starter Exploration Script

This script dynamically loads endpoints, calls them with example parameters, inspects returned DataFrames, and logs structure for building tests.

```python
# nba_api_explorer.py
import logging
from nba_api.stats.endpoints import (
    commonallplayers,
    commonteamyears,
    leaguegamefinder,
    playercareerstats,
    playergamelog,
    leaguedashplayerstats,
    leaguedashteamstats,
    teamgamefinder,
    boxscoretraditionalv3
)
import pandas as pd

# Configure logging
logging.basicConfig(filename='logs/nba_api_exploration.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of endpoints to explore with example parameters
endpoints = [
    (commonallplayers.CommonAllPlayers, {'is_only_current_season': 1, 'league_id': '00'}),
    (commonteamyears.CommonTeamYears, {'league_id': '00'}),
    (leaguegamefinder.LeagueGameFinder, {'league_id_nullable': '00'}),
    (playercareerstats.PlayerCareerStats, {'player_id': 2544}),  # LeBron James
    (playergamelog.PlayerGameLog, {'player_id': 2544, 'season': '2022-23', 'season_type_all_star': 'Regular Season'}),
    (leaguedashplayerstats.LeagueDashPlayerStats, {'season': '2022-23', 'season_type_all_star': 'Regular Season'}),
    (leaguedashteamstats.LeagueDashTeamStats, {'season': '2022-23', 'season_type_all_star': 'Regular Season'}),
    (teamgamefinder.TeamGameFinder, {'team_id_nullable': 1610612737, 'season_nullable': '2022-23'}),
    (boxscoretraditionalv3.BoxScoreTraditionalV3, {'game_id': '0022200017'})
]

# Iterate and explore
for endpoint_class, params in endpoints:
    try:
        ep = endpoint_class(**params)
        dfs = ep.get_data_frames()
        logging.info(f'Endpoint: {endpoint_class.__name__} | Returned {len(dfs)} DataFrame(s)')
        for i, df in enumerate(dfs):
            logging.info(f'DF #{i}: Columns: {list(df.columns)} | Sample: {df.head(1).to_dict()}')
        print(f"{endpoint_class.__name__} exploration complete. See logs for details.")
    except Exception as e:
        logging.error(f"Error calling {endpoint_class.__name__}: {str(e)}")
        print(f"{endpoint_class.__name__} failed. See logs for details.")

```

### Agent Instructions:

1.  Run the script in terminal:
    ```bash
    python nba_api_explorer.py
    ```
2.  Inspect logs at `logs/nba_api_exploration.log`
3.  Identify DataFrame columns and structures
4.  Create `.md` schema docs for each endpoint in `/docs/data_schemas/`
5.  Use these schemas to guide Phase 5 integration

---

## Step 5 — Create API Exploration Tests

Example test structure using `pytest`:

```python
import pytest
from nba_api.stats.endpoints import playercareerstats

def test_player_career_structure():
    df_list = playercareerstats.PlayerCareerStats(player_id="2544").get_data_frames()
    assert len(df_list) > 0
    df = df_list[0]
    assert "PLAYER_ID" in df.columns
    assert "SEASON_ID" in df.columns
```

Repeat for other endpoints. Ensure tests:
- Assert data frames exist
- Verify expected columns
- Log unexpected fields

---

## Step 6 — Data Schema Documentation

For each tested endpoint, generate `.md` docs in `/docs/data_schemas/`:

- `player_career_stats_schema.md`
- `player_game_log_schema.md`
- `team_stats_schema.md`
- `boxscore_traditional_schema.md`

Include:
- Endpoint class & URL
- Parameters
- Returned table names (resultSets)
- Column names and descriptions
- Sample row counts and types

---

## Phase Completion Criteria

Phase 4 is complete when:
- All core endpoints are tested
- Data schemas are documented in .md files
- Exploration tests validate structure
- Logs capture unexpected fields or errors

Phase 5 can only start after this.

---

End of Phase 4 Specification

---
