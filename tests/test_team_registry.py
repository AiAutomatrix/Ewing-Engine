def test_team_registry_consistency():
    from engine.data_ingestion.data_ingestion_runner import team_clean
    from engine.adapters.team_adapter import TeamAdapter
    from engine.simulation import Simulation

    teams = TeamAdapter(team_clean[0]).to_engine_objects()
    sim = Simulation(players=[], teams=teams, games=[], boxscores=[])

    for t in teams:
        assert t.id in sim.teams_by_id
        assert t.abbreviation in sim.teams_by_abbr
        assert sim.teams_by_id[t.id] is sim.teams_by_abbr[t.abbreviation]
