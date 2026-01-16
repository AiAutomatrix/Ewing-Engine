import re
import pandas as pd
from ast import literal_eval

log_file = 'logs/nba_api_exploration.log'

with open(log_file, 'r') as f:
    log_data = f.read()

# Split the log data by endpoint sections
endpoint_sections = re.split(r'\n(?=202\d-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - INFO - Endpoint:)', log_data)

boxscore_dataframes = []
player_stats_dataframes = []
team_stats_dataframes = []
game_finder_dataframes = []

for section in endpoint_sections:
    endpoint_match = re.search(r'Endpoint: (\w+)', section)
    if not endpoint_match:
        continue
    endpoint = endpoint_match.group(1)

    # Find all dataframe samples in the section
    samples = re.findall(r'Sample: (\{.*?\})(?=\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - INFO -|\Z)', section, re.DOTALL)
    for sample_str in samples:
        try:
            # literal_eval is safer than eval
            sample_dict = literal_eval(sample_str.replace(': nan', ': None'))
            df = pd.DataFrame(sample_dict)
            if not df.empty:
                if endpoint == "BoxScoreTraditionalV3":
                    boxscore_dataframes.append(df)
                elif endpoint in ["CommonAllPlayers", "PlayerCareerStats", "PlayerGameLog", "LeagueDashPlayerStats"]:
                    player_stats_dataframes.append(df)
                elif endpoint in ["CommonTeamYears", "LeagueDashTeamStats"]:
                    team_stats_dataframes.append(df)
                elif endpoint == "LeagueGameFinder":
                    game_finder_dataframes.append(df)
        except Exception as e:
            pass

with open('logs/phase4_data.py', 'w') as f:
    f.write('import pandas as pd\n\n')
    f.write(f'boxscore_dataframes_raw = {[df.to_dict("list") for df in boxscore_dataframes]}\n')
    f.write(f'player_stats_dataframes_raw = {[df.to_dict("list") for df in player_stats_dataframes]}\n')
    f.write(f'team_stats_dataframes_raw = {[df.to_dict("list") for df in team_stats_dataframes]}\n')
    f.write(f'game_finder_dataframes_raw = {[df.to_dict("list") for df in game_finder_dataframes]}\n')
