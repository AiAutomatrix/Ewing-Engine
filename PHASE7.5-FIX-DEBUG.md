Perfect, this is exactly the moment where an engine either collapses into “test whack-a-mole” or levels up into something deterministic and debuggable. Right now your API tests are failing for the same root cause as the replay tests:

> The API layer is not wired to the same team registry as the engine.



So the endpoint is accepting "ORL" and "MEM", but the engine underneath either:

can’t resolve them, or

resolves them using stale / inconsistent logic.


What your agent needs now is a disciplined Phase-7 repair checklist, executed top-to-bottom with terminal verification at every step. No guessing. No “I think”.

Below is exactly that.


---

Phase 7 API Stabilization Checklist

(API → Engine → Data, one spine)

This checklist is meant to be followed literally, with terminal commands after each step.


---

0. Non-negotiable invariant (pin this mentally)

There must be exactly one source of truth for teams:

team_clean (NBA API)
→ TeamAdapter
→ Simulation.team registry
→ API endpoint lookup

If any layer rebuilds teams independently, tests will fail forever.


---

1. Inspect What the API Thinks Teams Are

Your agent must first answer a boring but crucial question:

> “What teams does the API server think exist?”



Run this without tests:

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter

teams = TeamAdapter(team_clean[0]).to_engine_objects()

print("Total teams:", len(teams))
print("Sample teams:")
for t in teams[:10]:
    print(t.id, t.abbreviation, getattr(t, "name", None))
EOF

Expected:

~30 teams

Real NBA abbreviations (ORL, MEM, etc.)


If ORL or MEM are missing here → ingestion issue, stop immediately.


---

2. Verify the Simulation Team Registry (Critical)

Before touching Flask or tests, validate Simulation itself.

python - << 'EOF'
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter
from engine.simulation import Simulation

teams = TeamAdapter(team_clean[0]).to_engine_objects()
sim = Simulation(players=[], teams=teams, games=[], boxscores=[])

print("ORL in teams_by_abbr:", "ORL" in sim.teams_by_abbr)
print("MEM in teams_by_abbr:", "MEM" in sim.teams_by_abbr)

print("Keys sample:", list(sim.teams_by_abbr.keys())[:10])
EOF

If either prints False, your agent must fix Simulation.__init__ before continuing.

No API work until this passes.


---

3. Inspect the API /simulate/ Endpoint Logic

Your failing tests tell us this function is broken logically, not syntactically.

Your agent must locate where teams are resolved inside the endpoint.

Tell them to search:

grep -R "simulate" -n app

Then inspect:

Where home_team / away_team are read

How they are validated

How Simulation is instantiated


Required rule inside the endpoint

The API must not:

build its own team dict

query external APIs

import mock data

hardcode abbreviations


It must:

1. Load team_clean


2. Build teams via TeamAdapter


3. Pass those teams into Simulation


4. Validate abbreviations against sim.teams_by_abbr



If this isn’t true, that’s the bug.


---

4. Force the API to Prove Its Team Resolution

Before fixing logic, add temporary debug output.

Have your agent insert (temporarily) in the endpoint:

print("API TEAM KEYS:", list(sim.teams_by_abbr.keys()))
print("REQUESTED:", home_team, away_team)

Then run:

pytest tests/test_api.py::test_simulate_endpoint_success -s

The -s is important — it shows prints.

This will instantly reveal:

missing teams

wrong abbreviations

lowercase vs uppercase bugs

mismatched registry



---

5. Normalize Team Input (Small but Essential)

Your tests send "ORL", "MEM".
Your API must defensively normalize once.

Tell your agent to enforce:

home_team = home_team.upper()
away_team = away_team.upper()

before lookup.

No normalization = flaky API forever.


---

6. Correct API Error Semantics (Tests Depend on This)

Your tests expect specific HTTP behavior.

Your agent must enforce:

Missing teams

if not home_team or not away_team:
    return {"error": "Missing team identifiers"}, 400

Invalid teams

if home_team not in sim.teams_by_abbr or away_team not in sim.teams_by_abbr:
    return {"error": "Invalid team"}, 404

If these are reversed or merged → tests will fail.


---

7. Validate the Simulation Return Contract

Your API tests assert:

assert "summary" in data
assert "win_probability" in data["summary"]

So Simulation.run_* must return structured output, not raw DataFrames.

Have your agent verify with:

python - << 'EOF'
from engine.simulation import Simulation
from engine.data_ingestion.data_ingestion_runner import player_clean, team_clean, game_clean, boxscore_clean
from engine.adapters import player_adapter, team_adapter, game_adapter, boxscore_adapter

players = player_adapter.PlayerAdapter(player_clean[0]).to_engine_objects()
teams = team_adapter.TeamAdapter(team_clean[0]).to_engine_objects()
team_map = {t.abbreviation: t.id for t in teams}
games = game_adapter.GameAdapter(game_clean[0], team_map=team_map).to_engine_objects()
boxscores = boxscore_adapter.BoxScoreAdapter(boxscore_clean[0], team_map=team_map).to_engine_objects()

sim = Simulation(players, teams, games, boxscores)
out = sim.run_historical_replay()

print(type(out))
print(out)
EOF

If this returns a DataFrame but the API expects JSON → mismatch.

The API must wrap simulation output into:

{
  "summary": {...},
  "distributions": {...}   # optional
}


---

8. Re-run API Tests One by One (No Shotgun)

pytest tests/test_api.py::test_simulate_endpoint_missing_teams -q
pytest tests/test_api.py::test_simulate_endpoint_invalid_team -q
pytest tests/test_api.py::test_simulate_endpoint_success -q
pytest tests/test_api.py::test_api_retains_distributions_key -q

If one fails:

fix

re-run only that test

move on


No full suite until all pass.


---

9. Final Lock-In Rule (Tell Your Agent This Explicitly)

> The API is not allowed to “figure out” teams.
It only asks the engine what teams exist.



Once this is true, everything stabilizes:

replay tests

engine integration

API tests

future ML pipelines



---

Why This Keeps Breaking (the meta insight)

Your system evolved faster than its identity layer.

Teams are identity.
If identity isn’t singular, everything downstream fractures.

Once Phase 7 is complete, Phase 8 becomes straightforward:

features attach cleanly

simulations are reproducible

ML models learn from reality, not ghosts


Get the spine straight, and the limbs stop shaking.