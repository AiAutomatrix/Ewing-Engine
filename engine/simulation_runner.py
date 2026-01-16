import os
from engine.data_ingestion.data_ingestion_runner import player_clean, team_clean, game_clean, boxscore_clean
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

players = PlayerAdapter(player_clean[0]).to_engine_objects()
teams = TeamAdapter(team_clean[0]).to_engine_objects()
games = GameAdapter(game_clean[0]).to_engine_objects()
boxscores = BoxScoreAdapter(boxscore_clean[0]).to_engine_objects()

sim = Simulation(players=players, teams=teams, games=games, boxscores=boxscores)
results = sim.run_historical_replay()

# Export results to CSV
sim.export_to_csv(results, 'logs/historical_simulation.csv')

print("Simulation complete. Results saved to logs/historical_simulation.csv")
print(results.head())
