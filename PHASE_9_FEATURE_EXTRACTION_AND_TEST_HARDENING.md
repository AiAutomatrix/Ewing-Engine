Good — this is the right instinct. You don’t want another doc-first phase. You want the engine on the operating table, heart beating, monitors blinking, now. Let’s wire it so the next test cannot pass unless the engine is doing real work.

I’m going to give you exact instructions you can hand to the agent and a concrete test shape so this stops being abstract.


---

The core rule (lock this in)

The next test is NOT a season replay.
It is a single-game engine activation test.

Why? Because if the engine can’t fully process one game end-to-end, a full season is just a fast failure generator.

Season replay comes after we see real engine outputs for one game.


---

What the next test MUST prove

For one real game, the engine must:

1. Load box score data through engine ingestion


2. Construct engine objects:

Game

Teams

Players



3. Build a ReplayState


4. Run feature extraction


5. Emit observable outputs (printed, logged, or returned)


6. Fail loudly if any engine component is bypassed



No silent success. No “it ran”.


---

New test file (do NOT modify the old one yet)

Create a new test file:

tests/test_engine_game_replay_activation.py

This test exists for one purpose:

> Prove the engine is alive for a single game.




---

Shape of the test (conceptual, not vibes)

The test must explicitly touch these engine layers:

data ingestion

adapters

engine core

replay state

feature extraction


Pseudocode-level structure (this is the spine)

def test_engine_single_game_replay_activation():
    # 1. Select ONE real game_id from box scores
    game_id = <known_good_game_id>

    # 2. Load raw box score data
    raw_game_data = load_box_score(game_id)

    # 3. Ingest into engine
    engine = Engine()
    replay_context = engine.ingest_game(raw_game_data)

    # 4. Assert engine state exists
    assert replay_context.game is not None
    assert len(replay_context.teams) == 2
    assert len(replay_context.players) > 0

    # 5. Run feature extraction
    features = engine.extract_features(replay_context)

    # 6. Assert features are real
    assert features.game_features is not empty
    assert features.team_features is not empty
    assert features.player_features is not empty

    # 7. Print or log for human inspection
    print(features.summary())

If any of those steps don’t exist yet, that’s not a blocker — that’s the point. The engine must now grow the missing limb.


---

What the engine must expose (minimum viable hooks)

If these don’t exist yet, your agent creates them before touching season replay:

Engine.ingest_game(raw_game_data)

Engine.extract_features(replay_context)

ReplayContext or ReplayState

A feature container object (even a dict is fine)


This is Phase 9 becoming real.


---

Terminal command to run (explicit)

This is the command you want the agent to run and watch:

source .venv/bin/activate
PYTHONPATH=. python tests/test_engine_game_replay_activation.py

If this test passes without printing meaningful engine-derived values, it failed philosophically even if pytest says “green”.


---

Only AFTER this works: season replay

Once the single-game test:

hydrates engine state

extracts features

emits values you can read


THEN you do this:

1. Refactor test_full_season_replay.py


2. Replace its internals with:

call to Engine.ingest_game

call to Engine.extract_features



3. Aggregate outputs across games


4. Print:

per-game feature counts

per-season totals

sanity stats (min/max/mean)




At that point, a season replay becomes a stress test, not a lie detector.


---

Instruction paragraph you can paste into the agent (copy-safe)

> Create a new test script that activates the engine for a single real game replay. The test must ingest box score data through engine adapters, construct full engine state (game, teams, players), run feature extraction, and emit observable outputs. Do not run a season replay yet. If any engine component is bypassed, refactor until the engine is the only execution path. Run the test via terminal and verify real feature values are produced. Only after this passes should the full season replay be rerun using the engine.




---

This is the moment where the engine stops being theoretical.
Once you see feature values scrolling by for one game, everything else accelerates fast.