"""
Pytest tests for client API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from appointment_app.app import app

client = TestClient(app)

def test_create_client_success():
    response = client.post("/clients/", json={
        "client_id": "c1",
        "first_name": "Alice",
        "last_name": "Smith",
        "phone": "+34123456789",
        "email": "alice@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == "c1"
    assert data["first_name"] == "Alice"
    assert data["email"] == "alice@example.com"

def test_create_client_duplicate():
    client.post("/clients/", json={
        "client_id": "c2",
        "first_name": "Bob",
        "last_name": "Brown",
        "phone": "+34987654321",
        "email": "bob@example.com"
    })
    response = client.post("/clients/", json={
        "client_id": "c2",
        "first_name": "Bob",
        "last_name": "Brown",
        "phone": "+34987654321",
        "email": "bob@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Client ID already exists."

def test_get_client_success():
    client.post("/clients/", json={
        "client_id": "c3",
        "first_name": "Carol",
        "last_name": "White",
        "phone": "+34111222333",
        "email": "carol@example.com"
    })
    response = client.get("/clients/c3")
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == "c3"
    assert data["first_name"] == "Carol"

def test_get_client_not_found():
    response = client.get("/clients/unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found."
