# engine/replay_engine.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd

# Assuming these models are defined in engine/models.py
# and the get_simulation_instance is in engine/dependencies.py
from engine.models import Game, Team, Player, BoxScore
from engine.dependencies import get_simulation_instance


@dataclass
class ReplayState:
    """
    Holds the game-specific data for a single game replay.
    """
    game: Game
    teams: Dict[int, Team] = field(default_factory=dict)  # Teams involved in this specific game
    players: Dict[int, Player] = field(default_factory=dict) # Players involved in this specific game
    boxscores: List[BoxScore] = field(default_factory=list) # Boxscores for this specific game


@dataclass
class Features:
    """
    Holds extracted features for a single game replay.
    """
    game_features: Dict[str, Any] = field(default_factory=dict)
    team_features: Dict[int, Dict[str, Any]] = field(default_factory=dict) # Keyed by team_id
    player_features: Dict[int, Dict[str, Any]] = field(default_factory=dict) # Keyed by player_id
    game_id: Optional[str] = None # Added game_id for direct access in Features

    def summary(self) -> str:
        """
        Returns a human-readable summary of the extracted features.
        """
        summary_str = "\n--- Extracted Features Summary ---\n"
        if self.game_id:
            summary_str += f"For Game ID: {self.game_id}\n"
        
        summary_str += "Game Features:\n"
        for k, v in self.game_features.items():
            summary_str += f"  {k}: {v}\n"

        summary_str += "\nTeam Features (Home & Away):\n"
        # Determine home/away team_ids from game_features if available
        home_tid = self.game_features.get('home_team_id')
        away_tid = self.game_features.get('away_team_id')

        for team_id, features in self.team_features.items():
            team_type = ""
            if team_id == home_tid:
                team_type = "Home"
            elif team_id == away_tid:
                team_type = "Away"
            
            summary_str += f"  {team_type} Team (ID: {team_id}):\n"
            for k, v in features.items():
                summary_str += f"    {k}: {v}\n"

        summary_str += f"\nPlayer Features (first 5 players if many):\n"
        player_count = 0
        for player_id, features in self.player_features.items():
            if player_count >= 5:
                break
            summary_str += f"  Player (ID: {player_id}):\n"
            for k, v in features.items():
                summary_str += f"    {k}: {v}\n"
            player_count += 1
        if len(self.player_features) > 5:
            summary_str += f"  ... and {len(self.player_features) - 5} more players.\n"
        
        return summary_str


class Engine:
    """
    The core engine for managing simulation data and feature extraction.
    """
    def __init__(self, simulation_instance=None):
        self._simulation = simulation_instance if simulation_instance else get_simulation_instance()

        # Pre-build lookup maps for efficiency
        self._all_games_map: Dict[str, Game] = {game.id: game for game in self._simulation.games}
        self._all_teams_map: Dict[int, Team] = {team.id: team for team in self._simulation.teams}
        self._all_players_map: Dict[int, Player] = {player.id: player for player in self._simulation.players}

    def ingest_game(self, game_id: str) -> Optional[ReplayState]:
        """
        Ingests data for a specific game_id and returns a ReplayState.
        """
        game = self._all_games_map.get(game_id)
        if not game:
            print(f"Error: Game ID {game_id} not found in loaded games.")
            return None

        # Filter boxscores for the target game
        game_boxscores = [bs for bs in self._simulation.boxscores if bs.game_id == game_id]
        
        if not game_boxscores:
            print(f"Error: No box scores found for Game ID {game_id}.")
            return None

        # Collect unique team and player IDs involved in this game
        involved_team_ids = set()
        involved_player_ids = set()
        for bs in game_boxscores:
            involved_team_ids.add(bs.team_id)
            involved_player_ids.add(bs.player_id)
        
        # Add home/away teams from game object
        involved_team_ids.add(game.home_team)
        involved_team_ids.add(game.away_team)


        game_teams = {tid: self._all_teams_map[tid] for tid in involved_team_ids if tid in self._all_teams_map}
        game_players = {pid: self._all_players_map[pid] for pid in involved_player_ids if pid in self._all_players_map}
        
        # Also ensure players in game_players have relevant stats updated from boxscores
        for bs in game_boxscores:
            player = game_players.get(bs.player_id)
            if player:
                # Update player stats for this specific game's context
                # This could be more sophisticated, e.g., creating a new Player instance
                # or deep copying to avoid modifying global player objects.
                # For now, a direct update for demonstration.
                player.minutes = bs.minutes
                player.points = bs.pts
                player.rebounds = bs.rebounds
                player.assists = bs.assists
                player.steals = bs.steals if hasattr(bs, 'steals') else 0
                player.blocks = bs.blocks if hasattr(bs, 'blocks') else 0
                player.fg_pct = bs.fg_pct


        return ReplayState(game=game, teams=game_teams, players=game_players, boxscores=game_boxscores)

    def extract_features(self, replay_state: ReplayState) -> Features:
        """
        Extracts features from the given ReplayState.
        Populates with basic, observable features for auditing.
        """
        game = replay_state.game
        home_team = replay_state.teams.get(game.home_team)
        away_team = replay_state.teams.get(game.away_team)

        if not home_team or not away_team:
            print(f"Error: Home or Away team not found for game {game.id} in replay state.")
            return Features(game_id=game.id) # Return empty features with game_id

        # Game Features
        game_features = {
            "game_id": game.id,
            "game_date": game.date,
            "home_team_id": game.home_team,
            "away_team_id": game.away_team,
            "home_team_abbr": home_team.abbreviation,
            "away_team_abbr": away_team.abbreviation,
            "home_score_actual": self._simulation.game_scores.get(game.id, {}).get('home', 0),
            "away_score_actual": self._simulation.game_scores.get(game.id, {}).get('away', 0),
        }

        # Team Features (for home and away teams)
        team_features = {}
        for team_id in [game.home_team, game.away_team]: # Only process the two teams in the game
            team_obj = replay_state.teams.get(team_id)
            if team_obj:
                # Calculate team score from boxscores for this specific game
                team_score_in_game = sum(bs.pts for bs in replay_state.boxscores if bs.team_id == team_id)
                team_features[team_id] = {
                    "team_id": team_obj.id,
                    "team_name": team_obj.name,
                    "team_abbreviation": team_obj.abbreviation,
                    "team_pace_season_avg": team_obj.pace, # Example of a season-level feature
                    "team_off_rating_season_avg": team_obj.off_rating,
                    "team_def_rating_season_avg": team_obj.def_rating,
                    "team_score_in_game": team_score_in_game, # Feature for this game
                }

        # Player Features (for players in boxscores for this game)
        player_features = {}
        for player_id, player_obj in replay_state.players.items():
            # Find the boxscore entry for this player in this game to get per-game stats
            player_boxscore = next((bs for bs in replay_state.boxscores if bs.player_id == player_id), None)
            
            if player_boxscore:
                player_features[player_id] = {
                    "player_id": player_obj.id,
                    "player_name": player_obj.name,
                    "player_team_id_in_game": player_boxscore.team_id, # The team they played for in THIS game
                    "player_minutes_in_game": player_boxscore.minutes,
                    "player_points_in_game": player_boxscore.pts,
                    "player_rebounds_in_game": player_boxscore.rebounds,
                    "player_assists_in_game": player_boxscore.assists,
                    "player_fg_pct_in_game": player_boxscore.fg_pct,
                }
            else:
                # If a player is in replay_state.players but not in a boxscore (e.g., did not play)
                player_features[player_id] = {
                    "player_id": player_obj.id,
                    "player_name": player_obj.name,
                    "player_team_id_in_game": player_obj.team_id, # Default to their season team if not in boxscore
                    "player_minutes_in_game": 0,
                    "player_points_in_game": 0,
                    "player_rebounds_in_game": 0,
                    "player_assists_in_game": 0,
                    "player_fg_pct_in_game": 0.0,
                }


        return Features(
            game_id=game.id,
            game_features=game_features, 
            team_features=team_features, 
            player_features=player_features
        )