# engine/simulation.py

import numpy as np
import pandas as pd
from .config import SimulationConfig, default_config
from .models import SimulationModel, HeuristicModel, Player, Team, Game, BoxScore
from .game_log import GameLog
from .metrics import analyze_results

class Simulation:
    def __init__(self, players, teams, games, boxscores, config: SimulationConfig = None):
        self.players = players
        self.teams = teams
        self.teams_by_id = {team.id: team for team in teams}
        self.teams_by_abbr = {team.abbreviation: team for team in teams}
        self.games = sorted(games, key=lambda g: g.date)
        self.boxscores = boxscores
        self.game_scores = self._calculate_game_scores()
        self.config = config if config is not None else default_config
        if teams:
            self.league_avg_off_rating = np.mean([team.off_rating for team in teams])
        else:
            self.league_avg_off_rating = 110

    def _calculate_game_scores(self):
        scores = {}
        for game in self.games:
            home_score = sum(bs.pts for bs in self.boxscores if bs.game_id == game.id and bs.team_id == game.home_team)
            away_score = sum(bs.pts for bs in self.boxscores if bs.game_id == game.id and bs.team_id == game.away_team)
            if home_score > 0 or away_score > 0:
                 scores[game.id] = {'home': home_score, 'away': away_score}
        return scores

    def run_simulation_with_config(self, home_team_id: str = "GSW", away_team_id: str = "LAL", num_simulations: int = None, config: SimulationConfig = None, return_distributions: bool = False):
        current_config = config if config is not None else self.config
        if current_config.seed is not None:
            np.random.seed(current_config.seed)
        if num_simulations is None:
            num_simulations = current_config.default_num_simulations
        
        model_kwargs = {'league_avg_off_rating': self.league_avg_off_rating}
        if current_config.calibration:
            model_kwargs['calibration'] = current_config.calibration
        model = HeuristicModel(**model_kwargs)
        
        results = [self.simulate_game(model, home_team_id, away_team_id, current_config) for _ in range(num_simulations)]
        return analyze_results(results, return_distributions=return_distributions, config=current_config)

    def simulate_game(self, model: SimulationModel, home_team_id: str, away_team_id: str, config: SimulationConfig, log_game: bool = False):
        home_team = self.teams_by_abbr[home_team_id]
        away_team = self.teams_by_abbr[away_team_id]

        home_court_advantage = config.assumptions.home_court_advantage.value
        hca_off_bonus = home_court_advantage / 2.0
        hca_def_bonus = home_court_advantage / 2.0
        
        home_team_sim_stats = {
            "off_rating": home_team.off_rating + hca_off_bonus,
            "def_rating": home_team.def_rating - hca_def_bonus,
            "pace": home_team.pace,
            "efg_pct": home_team.efg_pct,
            "three_pt_rate": home_team.three_pt_rate,
            "ft_rate": home_team.ft_rate
        }
        
        away_team_sim_stats = {
            "off_rating": away_team.off_rating,
            "def_rating": away_team.def_rating,
            "pace": away_team.pace,
            "efg_pct": away_team.efg_pct,
            "three_pt_rate": away_team.three_pt_rate,
            "ft_rate": away_team.ft_rate
        }

        avg_pace = (home_team_sim_stats["pace"] + away_team_sim_stats["pace"]) / 2.0
        pace_modifier = config.pace_modifier if config.pace_modifier is not None else 1.0
        
        # Possession count is now clamped, and modifier is passed to scoring model
        final_pace = avg_pace # The modifier is applied in the model
        possession_count = int(np.random.normal(final_pace, config.pace_std_dev))
        possession_count = max(config.min_pace, min(config.max_pace, possession_count))

        home_score = 0
        away_score = 0

        for _ in range(possession_count // 2): 
            # Pass the pace_modifier to the scoring model
            points, _ = model.get_possession_outcome(home_team_sim_stats, away_team_sim_stats, config.assumptions, is_home=True, calibration=config.calibration, pace_modifier=pace_modifier)
            home_score += points

            points, _ = model.get_possession_outcome(away_team_sim_stats, home_team_sim_stats, config.assumptions, is_home=False, calibration=config.calibration, pace_modifier=pace_modifier)
            away_score += points

        return {
            "home_score": home_score,
            "away_score": away_score,
            "total_points": home_score + away_score,
            "winner": "home" if home_score > away_score else "away"
        }
    
    def run_single_historical_replay(self, game_id: str):
        if game_id not in self.game_scores:
            return None
        
        score = self.game_scores[game_id]
        return {
            'home_score_actual': score['home'],
            'away_score_actual': score['away']
        }
