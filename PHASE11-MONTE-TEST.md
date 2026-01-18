Perfect. This is a handoff document to your agent, not marketing copy, not theory. Clean, surgical, and unambiguous. Your agent should be able to execute Phase 11 without “interpreting intent.”

Below is the Phase 11 directive doc. You can paste this directly into your agent’s system or task instructions.


---

Phase 11 — Monte Carlo Sanity & Engine Life Test

Objective: Prove the simulation engine is stochastic, deterministic-when-seeded, and distribution-generating before any predictions or ML.


---

Phase 11 Purpose (Non-Negotiable)

Phase 11 exists to answer one question only:

> Does the engine produce variance-driven distributions instead of deterministic outcomes?



This phase does not care about accuracy, betting edges, or predictions.
It only validates that the simulation engine is alive.

If Phase 11 fails, Phase 12 is blocked.


---

Phase 11.1 — Single-Game Monte Carlo Sanity Test

(This is the FIRST test. No other Phase 11 work happens before this passes.)

Test Name

Phase 11.1 – Single-Game Monte Carlo Sanity Test


---

Test Setup

Game Selection

Choose ONE real, historical NBA game

Example: DEN vs LAL

Game must already be ingestible by the engine (no mock data)



---

Simulation Parameters

Simulations per run: 500

Engine configuration:

Fixed simulation config

No adaptive logic

No learning


Random seeds:

Seed A: 42

Seed B: 42 (control)

Seed C: 99




---

Execution Steps (Must Follow Exactly)

1. Boot the simulation engine normally

No hardcoded overrides

No replay shortcuts



2. Ingest the selected real game


3. Run 500 simulations with Seed = 42

Collect for each sim:

Home score

Away score

Winner




4. Aggregate and compute:

Mean home score

Mean away score

Standard deviation (home & away)

Home win rate



5. Repeat steps 3–4 with Seed = 42 again

Results must be identical



6. Repeat steps 3–4 with Seed = 99

Results must be different



7. Print all results to terminal/log output

Do NOT suppress or summarize away statistics





---

Required Output Format (Approximate Shape)

The exact numbers do not matter.
The structure and properties do.

--- Phase 11.1: Single-Game Monte Carlo Sanity Test ---
Game: DEN vs LAL
Simulations: 500

Run A (Seed = 42):
Home Mean: ###
Away Mean: ###
Home Std Dev: ###
Away Std Dev: ###
Home Win Rate: ###

Run B (Seed = 42, Control):
Home Mean: ###
Away Mean: ###
Home Std Dev: ###
Away Std Dev: ###
Home Win Rate: ###
Determinism Check: PASSED

Run C (Seed = 99):
Home Mean: ###
Away Mean: ###
Home Std Dev: ###
Away Std Dev: ###
Home Win Rate: ###
Variance Check: PASSED

Historical Result:
Actual Score: ###
Actual Winner: ###

Phase 11.1 Status: PASSED / FAILED


---

Pass / Fail Criteria

Phase 11.1 PASSES if ALL are true:

Standard deviation > 0 for both teams

Same seed → identical statistics

Different seed → different statistics

Mean scores are reasonably close to historical values

Home win rate is not 0% or 100%


Phase 11.1 FAILS if ANY occur:

Std dev = 0 (engine is deterministic)

Same seed produces different results

Different seed produces identical results

Win rate is degenerate (0% or 100%)

Scores explode or collapse unrealistically



---

Explicit Non-Goals of Phase 11

❌ No predictions

❌ No betting edges

❌ No machine learning

❌ No calibration

❌ No optimization


This phase only validates stochastic causal simulation.


---

Completion Rule

When Phase 11.1 completes:

1. Do not modify the engine


2. Do not add features


3. Do not tune parameters


4. Paste the full printed output back to the orchestrator (me)



Only after review will Phase 12 be authored.


---

Phase Transition Gate

Phase 11.1 PASS → Phase 12 unlocked

Phase 11.1 FAIL → engine debugging only, no forward progress



---

Mental Model (For the Agent)

Phase 11 proves the engine can generate possible worlds

Phase 12 teaches it to assign probabilities and expectations

ML comes after the engine proves it can simulate uncertainty



---

End of Phase 11 Directive

Once you run this and paste the output here, I’ll do two things immediately:

1. Audit the engine’s behavior (not just the numbers)


2. Author Phase 12, where:

Simulation turns into prediction

Calibration loops activate

ML is introduced safely (residual learning, not guesswork)




This is the right order.
You’re building a system, not a horoscope.