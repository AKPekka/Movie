"""Tests for the Flask application."""
import pytest
import json
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "cache" in data

def test_search_no_query(client):
    """Test search endpoint with no query."""
    response = client.get("/api/search")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_autocomplete_short_query(client):
    """Test autocomplete endpoint with short query."""
    response = client.get("/api/autocomplete?query=a")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["results"] == []

# Note: The following tests would require mocking the TMDb service
# or having a valid API key in the test environment

# def test_search_with_query(client):
#     """Test search endpoint with a valid query."""
#     response = client.get("/api/search?query=inception")
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert "results" in data
#     assert len(data["results"]) > 0

# def test_movie_details(client):
#     """Test getting movie details."""
#     # Inception movie ID
#     response = client.get("/api/movie/27205")
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert data["title"] == "Inception"

# def test_recommendations(client):
#     """Test movie recommendations."""
#     # Inception movie ID
#     response = client.get("/api/recommendations/movie/27205")
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert "results" in data
#     assert len(data["results"]) > 0
