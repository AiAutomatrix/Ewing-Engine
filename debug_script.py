from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter

teams = TeamAdapter(team_clean[0]).to_engine_objects()

print("Total teams:", len(teams))
print("Sample teams:")
for t in teams[:10]:
    print(t.id, t.abbreviation, getattr(t, "name", None))