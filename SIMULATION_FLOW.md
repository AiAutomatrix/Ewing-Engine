# SIMULATION_FLOW.md
## End-to-End Simulation Execution Flow

This document describes the exact execution order of the simulation engine.
The system must follow these steps in sequence.

---

### Step 1: Input Validation
Receive the following inputs:
- Home team identifier
- Away team identifier
- Optional simulation parameters:
  - number_of_simulations
  - random_seed

Validate:
- Teams exist in data
- Simulation count is within allowed bounds

---

### Step 2: Load Team Data
Load from data layer:
- Offensive rating
- Defensive rating
- Pace (possessions per game)
- Historical scoring efficiency

Prototype assumption:
- Team-level stats only
- No player-level substitutions yet

---

### Step 3: Estimate Possession Count
Calculate expected possessions using:
- Average of both teams’ pace
- Apply random variance (e.g. normal noise)

Clamp possessions to realistic bounds.

---

### Step 4: Initialize Simulation Loop
For each simulation iteration:

- Set scores to zero
- Set possession counter
- Alternate possession ownership

---

### Step 5: Simulate Possessions
For each possession:
- Determine offensive team
- Sample possession outcome using probability model
- Increment score accordingly
- Advance possession count

Stop when possession limit is reached.

---

### Step 6: Record Simulation Result
Store:
- Final home score
- Final away score
- Winner
- Total points

Do NOT compute aggregates yet.

---

### Step 7: Repeat
Repeat Steps 4–6 until all simulations are complete.

---

### Step 8: Aggregate Results
From all simulations:
- Compute win probability
- Compute score distributions
- Compute expected total points
- Compute standard deviation

---

### Step 9: Return Output Object
Return a structured object containing:
- Summary statistics
- Raw distributions (optional toggle)
- Metadata (simulation count, seed)

---

### Determinism Rule
If a random seed is provided:
- All results must be reproducible