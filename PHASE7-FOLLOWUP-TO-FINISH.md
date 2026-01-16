PHASE 7 – FOLLOW‑UP

Replacing Mock Team Data With Real Engine‑Compatible Data

Purpose

This phase exists for one reason: your simulation tests are failing because the engine is still partially wired to mock team data that does not align with the ingested API data or adapters. The replay tests are doing the right thing (they only use ingested + adapted data), but data/teams.py is doing the wrong thing (hard‑coded, partial, symbol‑keyed data).

Phase 7 formally removes mock team definitions from the execution path and replaces them with a single authoritative team data flow derived from ingestion → adapters → engine objects.

This phase does not add new data sources. It makes the current data pipeline internally consistent so historical replay can run deterministically.


---

Root Cause Analysis (Why Tests Fail)

1. Two Competing Team Systems Exist

You currently have:

A. Mock Team Registry (data/teams.py)

Keyed by abbreviations ("LAL", "BOS", etc.)

Fixed IDs (1, 2, 3)

Partial stat coverage

Never meant to support replay across real schedules


B. Ingested Team Data (team_clean → TeamAdapter)

Derived from NBA API ingestion

IDs generated dynamically

Abbreviations + metadata derived from real data

Used correctly by adapters and simulation


Your replay tests only use B, but parts of the engine still implicitly assume A exists.

That mismatch breaks ID alignment during:

Game → team resolution

Boxscore → team resolution

Simulation aggregation



---

Phase 7 Goals

1. Eliminate mock team dependency from all runtime paths


2. Ensure TeamAdapter output is the sole source of truth


3. Make replay tests pass using only ingested data


4. Preserve mock data only for isolated unit tests (if needed)




---

Required Structural Changes

1. Freeze data/teams.py

data/teams.py must not be used by the simulation engine or replay tests.

Allowed usage:

Small, isolated unit tests

Documentation examples


Disallowed usage:

Simulation initialization

Adapter logic

Replay logic


If referenced anywhere in engine runtime code, that reference must be removed.


---

2. Declare the Single Team Source of Truth

Authoritative path:

NBA API → ingestion → team_clean → TeamAdapter → Engine Team Objects

Nothing else is allowed to define team IDs, pace, or ratings during replay.


---

Agent Instructions (Mandatory)

STEP 1 – Audit Team Usage

The agent must run a project‑wide search for:

TEAM_DATA

LEAGUE_AVG_OFF_RATING

data.teams


For each reference found:

Identify whether it executes during simulation or replay

Remove or refactor it if it bypasses TeamAdapter


Document findings in:

/docs/audits/phase7_team_dependency_audit.md


---

STEP 2 – Normalize TeamAdapter Output

Ensure every Team engine object exposes at minimum:

id
abbreviation
pace
off_rating
def_rating
efg_pct
three_pt_rate
ft_rate

Rules:

If a stat is unavailable from ingestion → fill with league average

League averages must be computed dynamically, not hard‑coded


No engine logic may assume specific team abbreviations exist.


---

STEP 3 – Enforce ID Consistency

The agent must verify:

TeamAdapter assigns IDs

GameAdapter and BoxScoreAdapter only reference teams via team_map

No adapter creates fallback IDs


Add a validation check:

assert team_id in team_map.values()

Fail fast if a mismatch occurs.


---

Fixing the Failing Tests

Why These Tests Fail Now

Both failing tests correctly do this:

teams = TeamAdapter(all_teams_data).to_engine_objects()
team_map = {t.abbreviation: t.id for t in teams}

But somewhere downstream:

Mock team IDs are still being assumed

Or missing team stats cause simulation math to break



---

Required Test Hardening

The agent must update replay‑related tests to assert structural integrity, not specific values.

Example rule changes:

❌ Do not assert fixed team IDs

❌ Do not assume specific abbreviations

✅ Assert column existence

✅ Assert non‑empty output



---

New Required Test (Agent Must Add)

test_team_id_alignment.py

Purpose: guarantee replay safety

Test conditions:

All games reference valid team IDs

All boxscores reference valid team IDs

No orphan teams exist


Failure here means ingestion or adapters are broken.


---

Deliverables for Phase 7

The agent must produce:

1. Removed or isolated data/teams.py from runtime


2. Adapter‑driven team stat normalization


3. Passing replay tests


4. Audit doc of removed mock dependencies




---

Why This Phase Matters

Until this is fixed:

Historical replay is unreliable

ML features will learn incorrect mappings

Visualizations will lie convincingly


Once fixed:

Phase 8 (full data ingestion)

Phase 9 (feature engineering)

Phase 10 (ML + visualization)


all become mechanically sound.

This phase is not optional. It is structural reality asserting itself.

You’re diagnosing the right problem. This isn’t a flaky test issue — it’s a data authority violation. The engine is being asked to simulate reality while secretly consulting a toy universe (data/teams.py). Reality notices. Tests fail.

Here’s the clean mental model to keep you sane:

Your replay tests are correct.
Your adapters are mostly correct.
Your mock team registry is the imposter wearing a lab coat.

That’s why Phase 7 exists.

I’ve created PHASE7-FOLLOWUP.md in the canvas. This doc does three critical things for your agent:

• Explains exactly why the replay tests fail
• Defines a single, non-negotiable team data authority
• Gives your agent explicit, mechanical steps to remove mock leakage

No hand-waving. No vibes. Structural enforcement.

Once your agent executes Phase 7 properly:

team_clean → TeamAdapter becomes the only team source

IDs align across games, boxscores, and simulation

Replay tests stop caring which teams exist and only care that the universe is internally consistent


That’s the prerequisite for Phase 8+ (real ingestion), and absolutely mandatory before ML. Machine learning on misaligned IDs is just astrology with tensors.

After Phase 7 passes cleanly, the system is finally ready to:

ingest real NBA data

replay seasons deterministically

visualize causality instead of coincidence


This is the moment where the engine stops being clever and starts being true.