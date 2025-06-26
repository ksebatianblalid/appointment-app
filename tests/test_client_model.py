"""
Pytest tests for the Client Pydantic model.
"""
import pytest
from pydantic import ValidationError
from appointment_app.intranet.models.client import Client

def test_client_model_valid():
    c = Client(
        client_id="c10",
        first_name="Test",
        last_name="User",
        phone="+34000000000",
        email="test@example.com"
    )
    assert c.client_id == "c10"
    assert c.email == "test@example.com"

def test_client_model_invalid_email():
    with pytest.raises(ValidationError):
        Client(
            client_id="c11",
            first_name="Test",
            last_name="User",
            phone="+34000000000",
            email="not-an-email"
        )

def test_client_model_missing_field():
    with pytest.raises(ValidationError):
        Client(
            client_id="c12",
            first_name="Test",
            last_name="User",
            phone="+34000000000"
            # Missing email
        )
