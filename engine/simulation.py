# engine/simulation.py

import numpy as np
import pandas as pd
from .config import SimulationConfig, default_config
from .models import SimulationModel, HeuristicModel, Player, Team, Game, BoxScore
from .game_log import GameLog
from .metrics import analyze_results

class Simulation:
    def __init__(self, players, teams, games, boxscores):
        self.players = players
        self.teams = teams
        # Create two canonical maps for team lookups
        self.teams_by_id = {team.id: team for team in teams}
        self.teams_by_abbr = {team.abbreviation: team for team in teams}

        self.games = sorted(games, key=lambda g: g.date)
        self.boxscores = boxscores
        self.game_scores = self._calculate_game_scores()
        
        # Guard against division by zero if teams list is empty
        if teams:
            self.league_avg_off_rating = np.mean([team.off_rating for team in teams])
        else:
            self.league_avg_off_rating = 110 # A reasonable default

    def _calculate_game_scores(self):
        scores = {}
        for game in self.games:
            home_score = sum(bs.pts for bs in self.boxscores if bs.game_id == game.id and bs.team_id == game.home_team)
            away_score = sum(bs.pts for bs in self.boxscores if bs.game_id == game.id and bs.team_id == game.away_team)
            if home_score > 0 or away_score > 0:
                 scores[game.id] = {'home': home_score, 'away': away_score}
        return scores

    def run_historical_replay(self):
        results_list = []
        for game in self.games:
            if game.id not in self.game_scores:
                continue

            # Assertions to ensure data integrity
            assert game.home_team in self.teams_by_id, f"Home team ID {game.home_team} not found in team lookup"
            assert game.away_team in self.teams_by_id, f"Away team ID {game.away_team} not found in team lookup"

            home_team = self.teams_by_id[game.home_team]
            away_team = self.teams_by_id[game.away_team]

            # Run Monte Carlo simulation to get pre-game probabilities
            analysis = self.run_simulation_with_config(
                home_team_id=home_team.abbreviation,
                away_team_id=away_team.abbreviation
            )

            actual_scores = self.game_scores.get(game.id, {'home': 0, 'away': 0})

            results_list.append({
                'game_id': game.id,
                'home_team_id': game.home_team,
                'away_team_id': game.away_team,
                'home_score_actual': actual_scores['home'],
                'away_score_actual': actual_scores['away'],
                'win_probability_home': analysis.win_probability.get('home'),
                'win_probability_away': analysis.win_probability.get('away'),
                'expected_margin': analysis.expected_margin,
            })
        
        return pd.DataFrame(results_list)
    
    def export_to_csv(self, df, path):
        df.to_csv(path, index=False)

    def run_simulation_with_config(self, home_team_id: str = "GSW", away_team_id: str = "LAL", num_simulations: int = None, config: SimulationConfig = None, assumptions = None, return_distributions: bool = False):
        """Runs a Monte Carlo simulation with a given configuration."""
        if config is None:
            config = default_config
        
        if assumptions is not None:
            config.assumptions = assumptions
        
        if num_simulations is None:
            num_simulations = config.default_num_simulations

        model = HeuristicModel(league_avg_off_rating=self.league_avg_off_rating)
        results = [self.simulate_game(model, home_team_id, away_team_id, config) for _ in range(num_simulations)]
        return analyze_results(results, return_distributions=return_distributions)

    def simulate_game(self, model: SimulationModel, home_team_id: str, away_team_id: str, config: SimulationConfig, log_game: bool = False):
        # Look up teams by abbreviation
        home_team = self.teams_by_abbr[home_team_id]
        away_team = self.teams_by_abbr[away_team_id]
        game_log = GameLog(enabled=log_game)

        # Apply home court advantage from assumptions
        home_court_advantage = config.assumptions.home_court_advantage.value
        
        # Create simulation-specific copies of team data to avoid modifying originals
        home_team_sim_stats = {
            "off_rating": home_team.off_rating + home_court_advantage,
            "def_rating": home_team.def_rating,
            "pace": home_team.pace,
            "efg_pct": home_team.efg_pct,
            "three_pt_rate": home_team.three_pt_rate,
            "ft_rate": home_team.ft_rate,
        }
        away_team_sim_stats = {
            "off_rating": away_team.off_rating,
            "def_rating": away_team.def_rating,
            "pace": away_team.pace,
            "efg_pct": away_team.efg_pct,
            "three_pt_rate": away_team.three_pt_rate,
            "ft_rate": away_team.ft_rate,
        }

        # Determine game pace
        avg_pace = (home_team_sim_stats["pace"] + away_team_sim_stats["pace"]) / 2.0
        pace_modifier = config.assumptions.pace_modifier.value
        final_pace = avg_pace * pace_modifier

        possession_count = int(np.random.normal(final_pace, config.pace_std_dev))
        possession_count = max(config.min_pace, min(config.max_pace, possession_count))

        home_score = 0
        away_score = 0

        for i in range(possession_count):
            if i % 2 == 0:
                points, outcome = model.get_possession_outcome(home_team_sim_stats, away_team_sim_stats, config.assumptions)
                home_score += points
                game_log.record("home", outcome, points)
            else:
                points, outcome = model.get_possession_outcome(away_team_sim_stats, home_team_sim_stats, config.assumptions)
                away_score += points
                game_log.record("away", outcome, points)

        result = {
            "home_score": home_score,
            "away_score": away_score,
            "total_points": home_score + away_score,
            "winner": "home" if home_score > away_score else "away" if away_score > home_score else "draw"
        }

        if log_game:
            result["log"] = game_log.to_dict()
        
        return result
