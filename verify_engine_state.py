import pandas as pd
from engine.dependencies import get_simulation_instance
from engine.models import Player, Team, Game, BoxScore # Import models for type checking/clarity

def verify_simulation_loading():
    print("--- Initializing Simulation Instance ---")
    simulation = get_simulation_instance()
    print("Simulation instance initialized successfully.\n")

    print("--- Verifying Players ---")
    if simulation.players:
        print(f"Total Players loaded: {len(simulation.players)}")
        print("First 5 Players:")
        for player in simulation.players[:5]:
            print(f"  ID: {player.id}, Team ID: {player.team_id}, Name: {player.name}, Pts: {player.points}")
    else:
        print("No Players loaded.")
    print("-" * 40 + "\n")

    print("--- Verifying Teams ---")
    if simulation.teams:
        print(f"Total Teams loaded: {len(simulation.teams)}")
        print("First 5 Teams:")
        for team in simulation.teams[:5]:
            print(f"  ID: {team.id}, Abbreviation: {team.abbreviation}, Name: {team.name}")
    else:
        print("No Teams loaded.")
    print("-" * 40 + "\n")

    print("--- Verifying Games (Engine Objects) ---")
    if simulation.games:
        print(f"Total Games loaded: {len(simulation.games)}")
        print("First 5 Game Objects:")
        for game in simulation.games[:5]:
            print(f"  ID: {game.id}, Date: {game.date}, Home: {game.home_team}, Away: {game.away_team}")
    else:
        print("No Games loaded.")
    print("-" * 40 + "\n")

    print("--- Verifying Boxscores (Engine Objects) ---")
    if simulation.boxscores:
        print(f"Total BoxScores loaded: {len(simulation.boxscores)}")
        print("First 5 BoxScore Objects:")
        # Boxscores can be numerous; a sample is more appropriate.
        for bs in simulation.boxscores[:5]: # simulation.boxscores is a list
            print(f"  Game ID: {bs.game_id}, Team ID: {bs.team_id}, Player ID: {bs.player_id}, Pts: {bs.pts}")
    else:
        print("No BoxScores loaded.")
    print("-" * 40 + "\n")

if __name__ == "__main__":
    verify_simulation_loading()