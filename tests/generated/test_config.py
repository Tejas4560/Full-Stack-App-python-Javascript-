"""Tests for config module."""

import sys
import os
import pytest
from config import app
from models import Contact
from config import db
from unittest.mock import patch

sys.path.insert(0, r"/home/runner/work/Full-Stack-App-python-Javascript-/Full-Stack-App-python-Javascript-/pipeline/target_repo/backend")

@pytest.fixture(autouse=True)
def reset_database():
    """Reset the test database before each test."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def mock_verify_api_key(monkeypatch):
    monkeypatch.setenv("REQUIRE_API_KEY", "false")

@pytest.fixture
def mock_db_session(monkeypatch):
    from sqlalchemy.orm import Session

    class MockSession(Session):
        def execute(self, *args, **kwargs):
            raise Exception("Mocked session execute called unexpectedly.")

    session = MockSession(bind=None)
    monkeypatch.setattr("sqlalchemy.orm.Session", session)


class TestConfigIntegration:
    """Integration tests for config."""

    def test_get_contacts_empty(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test retrieving contacts when the database is empty."""
        response = client.get("/contacts")
        assert response.status_code == 200
        data = response.get_json()
        assert "contacts" in data
        assert isinstance(data["contacts"], list)
        assert len(data["contacts"]) == 0

    def test_get_contacts_with_data(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test retrieving contacts when there are entries in the database."""
        with app.app_context():
            contact1 = Contact(first_name="John", last_name="Doe", email="john@example.com")
            contact2 = Contact(first_name="Jane", last_name="Smith", email="jane@example.com")
            db.session.add(contact1)
            db.session.add(contact2)
            db.session.commit()

        response = client.get("/contacts")
        assert response.status_code == 200
        data = response.get_json()
        assert "contacts" in data
        assert isinstance(data["contacts"], list)
        assert len(data["contacts"]) == 2

    def test_create_contact_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test creating a contact successfully."""
        payload = {
            "firstName": "Alice",
            "lastName": "Wonderland",
            "email": "alice@example.com"
        }
        response = client.post("/create_contact", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "User created!"

    @pytest.mark.parametrize(
        "payload, error_message",
        [
            ({"firstName": "Alice"}, "You must include a first name, last name and email"),
            ({"firstName": "Bob", "lastName": "Builder"}, "You must include a first name, last name and email"),
            ({}, "You must include a first name, last name and email"),
        ]
    )
    def test_create_contact_failure(self, client, payload, error_message):
        """UNIVERSAL test for maximum coverage."""
        """Test creating a contact with missing fields."""
        response = client.post("/create_contact", json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert "message" in data
        assert data["message"] == error_message

    def test_update_contact_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test updating an existing contact."""
        with app.app_context():
            contact = Contact(first_name="Charlie", last_name="Brown", email="charlie@example.com")
            db.session.add(contact)
            db.session.commit()
            contact_id = contact.id

        payload = {"firstName": "Charles"}
        response = client.patch(f"/update_contact/{contact_id}", json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "Usr updated."

    def test_update_contact_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test updating a contact that does not exist."""
        payload = {"firstName": "NonExistent"}
        response = client.patch("/update_contact/9999", json=payload)
        assert response.status_code == 404
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "User not found"

    def test_delete_contact_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test deleting an existing contact."""
        with app.app_context():
            contact = Contact(first_name="Eve", last_name="Smith", email="eve@example.com")
            db.session.add(contact)
            db.session.commit()
            contact_id = contact.id

        response = client.delete(f"/delete_contact/{contact_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "User deleted!"

    def test_delete_contact_not_found(self, client, mock_verify_api_key, mock_db_session):
        """Test deleting a contact that does not exist."""
        response = client.delete('/delete_contact/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'User not found'

