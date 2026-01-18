
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter

all_teams = []
for team_df in team_clean:
    teams = TeamAdapter(team_df).to_engine_objects()
    all_teams.extend(teams)

print("Total teams:", len(all_teams))
for t in all_teams:
    print(t.id, t.abbreviation, t.name)
