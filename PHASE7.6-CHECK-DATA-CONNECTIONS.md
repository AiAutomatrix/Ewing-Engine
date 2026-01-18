Excellent — this is exactly the moment where projects either snap into coherence or quietly rot. You’re doing the right thing by forcing reality checks via terminal output instead of trusting assumptions.

Below is Phase 7.6, written explicitly as agent marching orders. This is not conceptual guidance — it is a procedural debug protocol. Your agent should follow it linearly, run the commands exactly, and save outputs.


---

PHASE 7.6 — DATA-ONLY ENGINE VALIDATION & TEST RECONCILIATION

Objective
Eliminate all remaining mock-data assumptions. Validate that every test, every adapter, and every API route is operating exclusively on real ingested NBA API data.

No refactors unless terminal evidence demands it.


---

RULES (NON-NEGOTIABLE)

1. No mock data files (teams.py, hardcoded dicts, constants).


2. No silent fixes — every fix must be justified by terminal output.


3. Every failing test must be reproducible in isolation.


4. Every terminal command must be copy-pasted exactly.


5. Save outputs to /logs/phase7_6_debug/.




---

STEP 0 — ENVIRONMENT SANITY CHECK

Run from project root:

pwd
python --version
pytest --version

Save output to:

logs/phase7_6_debug/env.txt


---

STEP 1 — VERIFY INGESTED DATA OBJECTS (GROUND TRUTH)

1.1 Teams (authoritative source)

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter

teams = TeamAdapter(team_clean[0]).to_engine_objects()

print("Total teams:", len(teams))
for t in teams:
    print(t.id, t.abbreviation, t.name)
EOF

Expected

~30 teams

Valid NBA IDs (16106127xx)

Non-empty abbreviations and names


Save to:

logs/phase7_6_debug/teams.txt

❌ If fewer than 30 teams → ingestion filtering bug
❌ If abbreviations missing → adapter bug
❌ If names missing → ingestor regression

Stop immediately if this fails.


---

STEP 2 — BUILD AND VALIDATE TEAM MAP (CRITICAL)

Every downstream failure depends on this mapping.

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter

teams = TeamAdapter(team_clean[0]).to_engine_objects()
team_map = {t.abbreviation: t.id for t in teams}

print("Team map size:", len(team_map))
print("Sample mappings:")
for k in list(team_map.keys())[:10]:
    print(k, "->", team_map[k])
EOF

Save to:

logs/phase7_6_debug/team_map.txt

If ORL, MEM, ATL, etc. are missing → API tests will fail.


---

STEP 3 — GAME ADAPTER VALIDATION

Games must reference teams by abbreviation → ID mapping.

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import game_clean, team_clean
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter

teams = TeamAdapter(team_clean[0]).to_engine_objects()
team_map = {t.abbreviation: t.id for t in teams}

games = GameAdapter(game_clean[0], team_map=team_map).to_engine_objects()

print("Total games:", len(games))
g = games[0]
print("Sample game:")
print("Game ID:", g.id)
print("Home team ID:", g.home_team_id)
print("Away team ID:", g.visitor_team_id)
EOF

Save to:

logs/phase7_6_debug/games.txt

❌ If KeyError on abbreviation → adapter logic wrong
❌ If home/away IDs are None → mapping failure


---

STEP 4 — BOXSCORE ADAPTER VALIDATION

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import boxscore_clean, team_clean
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter

teams = TeamAdapter(team_clean[0]).to_engine_objects()
team_map = {t.abbreviation: t.id for t in teams}

boxscores = BoxScoreAdapter(boxscore_clean[0], team_map=team_map).to_engine_objects()

print("Total boxscore rows:", len(boxscores))
b = boxscores[0]
print(vars(b))
EOF

Save to:

logs/phase7_6_debug/boxscores.txt


---

STEP 5 — SIMULATION CORE (NO API, NO TESTS)

This isolates engine logic.

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import player_clean, team_clean, game_clean, boxscore_clean
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

players = PlayerAdapter(player_clean[0]).to_engine_objects()
teams = TeamAdapter(team_clean[0]).to_engine_objects()
team_map = {t.abbreviation: t.id for t in teams}
games = GameAdapter(game_clean[0], team_map=team_map).to_engine_objects()
boxscores = BoxScoreAdapter(boxscore_clean[0], team_map=team_map).to_engine_objects()

sim = Simulation(players, teams, games, boxscores)
results = sim.run_historical_replay()

print(results.head())
print("Columns:", list(results.columns))
print("Rows:", len(results))
EOF

Save to:

logs/phase7_6_debug/simulation.txt

❌ If this fails → engine logic bug
✅ If this works → tests/API are wiring issues only


---

STEP 6 — TESTS IN ISOLATION (MANDATORY)

Run tests one file at a time.

pytest tests/test_engine_integration.py -q
pytest tests/test_simulation_replay.py -q
pytest tests/test_api.py -q

After each failure:

Copy traceback

Identify first missing assumption

Fix adapter or simulation — not tests


Save outputs:

logs/phase7_6_debug/test_engine_integration.txt
logs/phase7_6_debug/test_simulation_replay.txt
logs/phase7_6_debug/test_api.txt


---

STEP 7 — API ROUTE VALIDATION (REAL DATA ONLY)

python - << 'EOF'
from app import create_app
app = create_app()
client = app.test_client()

resp = client.post("/simulate/", json={
    "home_team": "ORL",
    "away_team": "MEM",
    "num_simulations": 10
})

print("Status:", resp.status_code)
print(resp.json)
EOF

If this fails:

The issue is team lookup inside API handler

Fix must use team_map built from ingestion — never constants



---

COMPLETION CRITERIA (PHASE 7.6)

✅ No mock data files exist
✅ All adapters use ingested schemas
✅ Simulation works standalone
✅ All pytest files pass
✅ /simulate works for real teams
✅ Logs saved for auditability


---

IMPORTANT PHILOSOPHICAL NOTE (FOR YOUR AGENT)

At this stage, tests do not define truth.
Ingested data does.

If a test fails but terminal data proves correctness, the test is wrong.


---

Once Phase 7.6 is clean, Phase 8 (ML + visualization) becomes boringly straightforward — which is exactly how you want it.

If you want, next we can:

Lock schemas with contracts

Generate feature matrices

Build replay-based labels for supervised learning


But first: reality must pass its exams.

You’re actually in a very good place. Phase 7.6 is no longer about “why is this broken?” — it’s about hardening the pipeline and converting all remaining tests from toy data to real, persisted data. The mistakes your agent made at the end are structural, not conceptual, which is good news.

What you want now are clear, authoritative marching orders for a fresh agent so it doesn’t thrash or re-invent work.

Below are precise instructions you can give your agent for Phase 7.6, step-by-step, framed as an engineering mandate rather than vague guidance.


---

Phase 7.6 – Agent Instructions (Authoritative)

Core Rule (Non-Negotiable)

All tests must run against real persisted data.
Mock data is forbidden beyond unit-level schema tests.

If a test currently depends on logs/phase4_data.py, it must be rewritten to load from data/processed/*.parquet.


---

Step 1 — Freeze the Data Contract (DO NOT SKIP)

Objective: Lock in what “real data” means so tests stop drifting.

Tell the agent:

> Before touching any tests, inspect and document the actual schemas produced by the ingestion pipeline.



Required terminal commands

ls data/processed
python - << 'EOF'
import pandas as pd
df = pd.read_parquet("data/processed/game_finder_0.parquet")
print(df.columns)
print(df.head(2))
EOF

Repeat for:

boxscore_*.parquet

(later) player stats

team stats


Deliverable:
A short markdown or text file:

docs/phase7_6/data_contract.md

Containing:

File name

Columns

Primary keys

Expected row counts (order of magnitude)


This becomes the single source of truth for tests.


---

Step 2 — Fix the BoxScoreIngestor (Critical Bug)

Your agent’s last edit broke the class entirely (logic inside __init__, missing ingest, missing BaseIngestor init).

Tell the agent explicitly:

> Restore BoxScoreIngestor to a valid class shape.
__init__ must only initialize state.
All ingestion logic must live in ingest().



Structural checklist

class BoxScoreIngestor(BaseIngestor)

__init__ calls super().__init__

ingest(self, game_ids) exists

Retry logic is inside ingest

Progress logging every N games (not every game)


Mandatory guardrails

Sleep between requests (e.g. 0.6–1.0s)

Max retries per game

Collect failures into a list and persist them


Deliverable:
data/processed/boxscore_failures.json

This is observability, not noise.


---

Step 3 — Make the Runner Idempotent

Right now, rerunning the pipeline re-downloads everything.

Tell the agent:

> Update data_ingestion_runner.py so it skips work when parquet files already exist unless a --force flag is passed.



Required behavior

If data/processed/game_finder_0.parquet exists → skip GameFinder

If boxscore parquet exists → only ingest missing game_ids

Print exactly what is skipped and why


This prevents:

Hanging terminals

API abuse

Developer panic



---

Step 4 — Convert Tests to Real Data

This is the actual goal of Phase 7.6.

Tell the agent:

> Every remaining test must load from data/processed, not from logs/phase4_data.py.



Pattern to enforce

Replace:

from logs.phase4_data import team_stats_dataframes_raw

With:

pd.read_parquet("data/processed/team_stats_0.parquet")

Test categories to fix

TeamAdapter tests

PlayerAdapter tests

Simulation engine tests

Any test asserting counts, IDs, joins


Rule

Tests may assert structure and invariants, not exact row counts:

len(df) > 0

game_id is unique

team_id maps to name

joins do not explode row counts



---

Step 5 — Explicit “No Mock” Enforcement

Tell the agent to add a guard:

> If any test imports logs.phase4_data, the test must fail immediately.



Example pattern:

assert "logs/phase4_data" not in sys.modules

This prevents regressions later.


---

Step 6 — Controlled PlayerStats Ingestion (VERY IMPORTANT)

Your agent was about to accidentally DDoS itself.

Tell it clearly:

> PlayerStats ingestion must be batched and sampled, not full-league by default.



Rules

Default: sample 100–200 players max

Player IDs derived from boxscore parquet

Full ingestion requires explicit flag


Why:

Career stats endpoints are slow

Phase 7.6 is validation, not full ML training



---

Step 7 — Phase 7.6 Exit Criteria (Definition of Done)

Tell the agent Phase 7.6 is complete only when:

1. data_ingestion_runner.py completes without hanging


2. All tests pass using real parquet data


3. No test imports mock data


4. Failures are logged, not swallowed


5. Rerunning ingestion is safe and fast




---

Meta-Insight (Why This Matters)

What you’re building now is no longer “data ingestion” — it’s data gravity.

Once:

Real data is persisted

Tests bind to that reality

Ingestors become idempotent


…the engine stops being fragile. At that point, ML, simulation, and strategy layers stop fighting the substrate.

Phase 7.6 is the moment your engine stops pretending to be real and actually becomes real.

When you’re ready, the next phase is schema versioning + backfill strategy, which is where serious systems graduate from “project” to “platform”.