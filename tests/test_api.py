# tests/test_api.py

import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_simulate_endpoint_success(client):
    """Tests a successful simulation request."""
    response = client.post("/simulate/", json={
        "home_team": "ORL",
        "away_team": "MEM",
        "num_simulations": 10,
        "random_seed": 42
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "summary" in data
    assert "win_probability" in data["summary"]

def test_simulate_endpoint_missing_teams(client):
    """Tests that the endpoint fails without team identifiers."""
    response = client.post("/simulate/", json={})
    assert response.status_code == 400

def test_simulate_endpoint_invalid_team(client):
    """Tests that the endpoint fails with an invalid team ID."""
    response = client.post("/simulate/", json={
        "home_team": "INVALID",
        "away_team": "ORL"
    })
    assert response.status_code == 404

def test_api_retains_distributions_key(client):
    """ 
    Tests that the API response includes the 'distributions' key when requested,
    even after the introduction of the metrics module.
    """
    response = client.post("/simulate/", json={
        "home_team": "ORL",
        "away_team": "MEM",
        "num_simulations": 10,
        "return_distributions": True
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "distributions" in data
