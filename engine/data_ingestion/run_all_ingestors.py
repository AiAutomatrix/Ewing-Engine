
import subprocess

# Define the order of ingestion scripts
ingestion_scripts = [
    "engine/data_ingestion/ingest_teams.py",
    "engine/data_ingestion/ingest_players.py",
    "engine/data_ingestion/ingest_games.py",
    "engine/data_ingestion/ingest_boxscores.py",
]

# Run each ingestion script
for script in ingestion_scripts:
    print(f"--- Running {script} ---")
    subprocess.run(["python", script], check=True)

print("\n--- All data ingestion complete. ---")
