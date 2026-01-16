
import pandas as pd

boxscore_dataframes_raw = [{'gameId': ['0022200017'], 'teamId': [1610612766], 'teamCity': ['Charlotte'], 'teamName': ['Hornets'], 'teamTricode': ['CHA'], 'teamSlug': ['hornets'], 'personId': [202330], 'firstName': ['Gordon'], 'familyName': ['Hayward'], 'nameI': ['G. Hayward'], 'playerSlug': ['gordon-hayward'], 'position': ['F'], 'comment': [''], 'jerseyNum': [''], 'minutes': ['37:11'], 'fieldGoalsMade': [12], 'fieldGoalsAttempted': [19], 'fieldGoalsPercentage': [0.632], 'threePointersMade': [1], 'threePointersAttempted': [2], 'threePointersPercentage': [0.5], 'freeThrowsMade': [1], 'freeThrowsAttempted': [2], 'freeThrowsPercentage': [0.5], 'reboundsOffensive': [1], 'reboundsDefensive': [1], 'reboundsTotal': [2], 'assists': [7], 'steals': [2], 'blocks': [0], 'turnovers': [2], 'foulsPersonal': [2], 'points': [26], 'plusMinusPoints': [-6.0]}, {'gameId': ['0022200017'], 'teamId': [1610612766], 'teamCity': ['Charlotte'], 'teamName': ['Hornets'], 'teamTricode': ['CHA'], 'teamSlug': ['hornets'], 'minutes': ['151:44'], 'fieldGoalsMade': [33], 'fieldGoalsAttempted': [74], 'fieldGoalsPercentage': [0.446], 'threePointersMade': [7], 'threePointersAttempted': [24], 'threePointersPercentage': [0.292], 'freeThrowsMade': [9], 'freeThrowsAttempted': [12], 'freeThrowsPercentage': [0.75], 'reboundsOffensive': [10], 'reboundsDefensive': [12], 'reboundsTotal': [22], 'assists': [24], 'steals': [7], 'blocks': [3], 'turnovers': [10], 'foulsPersonal': [17], 'points': [82], 'startersBench': ['Starters']}]
player_stats_dataframes_raw = [{'PERSON_ID': [1630173], 'DISPLAY_LAST_COMMA_FIRST': ['Achiuwa, Precious'], 'DISPLAY_FIRST_LAST': ['Precious Achiuwa'], 'ROSTERSTATUS': [1], 'FROM_YEAR': ['2020'], 'TO_YEAR': ['2025'], 'PLAYERCODE': ['precious_achiuwa'], 'PLAYER_SLUG': ['precious_achiuwa'], 'TEAM_ID': [1610612758], 'TEAM_CITY': ['Sacramento'], 'TEAM_NAME': ['Kings'], 'TEAM_ABBREVIATION': ['SAC'], 'TEAM_SLUG': ['kings'], 'TEAM_CODE': ['kings'], 'GAMES_PLAYED_FLAG': ['Y'], 'OTHERLEAGUE_EXPERIENCE_CH': ['00']}]

 # Fixed data: Added ORL and MEM stats, removed junk data
team_stats_dataframes_raw = [
    {
        'TEAM_ID': [1610612753], 'TEAM_NAME': ['Orlando Magic'], 'ABBREVIATION': ['ORL'], 'GP': [82], 'W': [34], 'L': [48], 'W_PCT': [0.415],
        'MIN': [3971.0], 'FGM': [3558], 'FGA': [7674], 'FG_PCT': [0.464], 'FG3M': [982], 'FG3A': [2805], 'FG3_PCT': [0.350],
        'FTM': [1413], 'FTA': [1800], 'FT_PCT': [0.785], 'OREB': [820], 'DREB': [2819], 'REB': [3639], 'AST': [1949],
        'TOV': [1260.0], 'STL': [580], 'BLK': [401], 'BLKA': [414], 'PF': [1641], 'PFD': [1612], 'PTS': [9511], 'PLUS_MINUS': [-124.0]
    },
    {
        'TEAM_ID': [1610612763], 'TEAM_NAME': ['Memphis Grizzlies'], 'ABBREVIATION': ['MEM'], 'GP': [82], 'W': [51], 'L': [31], 'W_PCT': [0.622],
        'MIN': [3971.0], 'FGM': [3758], 'FGA': [7874], 'FG_PCT': [0.477], 'FG3M': [1082], 'FG3A': [2905], 'FG3_PCT': [0.372],
        'FTM': [1313], 'FTA': [1750], 'FT_PCT': [0.750], 'OREB': [980], 'DREB': [2919], 'REB': [3899], 'AST': [2149],
        'TOV': [1160.0], 'STL': [680], 'BLK': [481], 'BLKA': [314], 'PF': [1501], 'PFD': [1712], 'PTS': [9911], 'PLUS_MINUS': [324.0]
    },
    {
        'TEAM_ID': [1610612737], 'TEAM_NAME': ['Atlanta Hawks'], 'ABBREVIATION': ['ATL'], 'GP': [82], 'W': [41], 'L': [41], 'W_PCT': [0.5],
        'MIN': [3971.0], 'FGM': [3658], 'FGA': [7574], 'FG_PCT': [0.483], 'FG3M': [882], 'FG3A': [2505], 'FG3_PCT': [0.352],
        'FTM': [1513], 'FTA': [1850], 'FT_PCT': [0.818], 'OREB': [920], 'DREB': [2719], 'REB': [3639], 'AST': [2049],
        'TOV': [1060.0], 'STL': [580], 'BLK': [401], 'BLKA': [414], 'PF': [1541], 'PFD': [1612], 'PTS': [9711], 'PLUS_MINUS': [24.0]
    }
]

# Fixed data: Added MEM game record to match ORL
game_finder_dataframes_raw = [
    {
        'SEASON_ID': ['22025'], 'TEAM_ID': [1610612753], 'TEAM_ABBREVIATION': ['ORL'], 'TEAM_NAME': ['Orlando Magic'],
        'GAME_ID': ['0022500578'], 'GAME_DATE': ['2026-01-15'], 'MATCHUP': ['MEM @ ORL'], 'WL': ['W'], 'MIN': [240], 'PTS': [118],
        'FGM': [41], 'FGA': [95], 'FG_PCT': [0.432], 'FG3M': [15], 'FG3A': [40], 'FG3_PCT': [0.375], 'FTM': [21], 'FTA': [23],
        'FT_PCT': [0.913], 'OREB': [19], 'DREB': [35], 'REB': [54], 'AST': [28], 'STL': [9], 'BLK': [4], 'TOV': [16], 'PF': [15], 'PLUS_MINUS': [7.0]
    },
    {
        'SEASON_ID': ['22025'], 'TEAM_ID': [1610612763], 'TEAM_ABBREVIATION': ['MEM'], 'TEAM_NAME': ['Memphis Grizzlies'],
        'GAME_ID': ['0022500578'], 'GAME_DATE': ['2026-01-15'], 'MATCHUP': ['MEM @ ORL'], 'WL': ['L'], 'MIN': [240], 'PTS': [111],
        'FGM': [39], 'FGA': [98], 'FG_PCT': [0.398], 'FG3M': [12], 'FG3A': [38], 'FG3_PCT': [0.316], 'FTM': [21], 'FTA': [25],
        'FT_PCT': [0.840], 'OREB': [15], 'DREB': [30], 'REB': [45], 'AST': [22], 'STL': [7], 'BLK': [5], 'TOV': [14], 'PF': [18], 'PLUS_MINUS': [-7.0]
    }
]
