import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_suggest_endpoint_validation():
    """Test meal suggestion endpoint validation."""
    # Test empty message
    response = client.post("/api/chat/suggest", json={"message": ""})
    assert response.status_code == 422  # Validation error
    
    # Test missing message
    response = client.post("/api/chat/suggest", json={})
    assert response.status_code == 422  # Validation error


def test_suggest_endpoint_without_api_key():
    """Test meal suggestion endpoint without API key (should fail gracefully)."""
    response = client.post(
        "/api/chat/suggest", 
        json={"message": "I want a healthy meal"}
    )
    # This will fail due to missing API key, but should return 500, not crash
    assert response.status_code == 500
    data = response.json()
    assert data["success"] is False
