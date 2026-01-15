# API_CONTRACT.md
## Backend Simulation API Contract

This document defines how the frontend or external systems
interact with the simulation engine.

---

### Endpoint: /simulate

Method: POST  
Content-Type: application/json

---

### Request Body

```json
{
  "home_team": "LAL",
  "away_team": "BOS",
  "num_simulations": 10000,
  "random_seed": 42,
  "return_distributions": true
}