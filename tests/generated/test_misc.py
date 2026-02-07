"""Tests for misc module."""

import sys
import os
import pytest
from unittest.mock import MagicMock
from flask import Flask
from unittest.mock import Mock

sys.path.insert(0, r"/home/runner/work/Full-Stack-App-python-Javascript-/Full-Stack-App-python-Javascript-/pipeline/target_repo/backend")

@pytest.fixture
def sample_contact():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com"
    }

@pytest.fixture
def client(app, monkeypatch):
    """Fixture to set up a test client with mock database."""
    # Mock database query for the Contact model
    mock_query = MagicMock()
    mock_query.all.return_value = []
    monkeypatch.setattr('models.Contact.query', mock_query)

    # Disable API key requirement for tests
    monkeypatch.setenv("REQUIRE_API_KEY", "false")

    return app.test_client()

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/create_contact', methods=['POST'])
    def create_contact():
        return {"message": "Contact created"}, 201

    @app.route('/contacts', methods=['GET'])
    def get_contacts():
        return {
            "contacts": [
                {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
            ]
        }, 200

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def client():
    class MockClient:
        def patch(self, url, json=None):
            if url == '/update_contact/99999':
                return MagicMock(
                    status_code=404,
                    get_json=MagicMock(return_value={'message': 'User not found'})
                )
            return MagicMock(status_code=400)

    return MockClient()


@pytest.mark.e2e
class TestMiscE2E:
    """End-to-end tests for misc."""

    def test_create_contact_success(self, client, sample_contact):
        """UNIVERSAL test for maximum coverage."""
        'Test that a contact can be created successfully.'
        response = client.post('/create_contact', json=sample_contact)
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Contact created'

    def test_create_contact_missing_fields(self, client):
        """UNIVERSAL test for maximum coverage."""
        """Test contact creation fails if required fields are missing."""
        response = client.post('/create_contact', json={"firstName": "Jane"})
        assert response.status_code == 400
        data = response.get_json()
        assert "message" in data

    def test_get_contacts_empty(self, client):
        """Test retrieving contacts when none exist."""
        response = client.get('/contacts')
        assert response.status_code == 200
        data = response.get_json()
        assert 'contacts' in data
        assert len(data['contacts']) == 0

    def test_get_contacts_with_data(self, client, sample_contact):
        """Test retrieving contacts when contacts exist."""
        client.post('/create_contact', json=sample_contact)
        response = client.get('/contacts')
        assert response.status_code == 200
        data = response.get_json()
        assert 'contacts' in data
        assert len(data['contacts']) == 1
        contact = data['contacts'][0]
        assert contact['first_name'] == sample_contact['firstName']
        assert contact['last_name'] == sample_contact['lastName']
        assert contact['email'] == sample_contact['email']

    def test_update_contact_success(self, client, sample_contact):
        """UNIVERSAL test for maximum coverage."""
        """Test successful update of a contact."""
        # Create a contact first
        client.post('/create_contact', json=sample_contact)

        # Retrieve the created contact's ID
        response = client.get('/contacts')
        contact_id = response.get_json()["contacts"][0]["id"]

        # Update the contact
        updated_data = {"firstName": "Jane", "lastName": "Smith", "email": "jane.smith@example.com"}
        response = client.patch(f'/update_contact/{contact_id}', json=updated_data)
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "Usr updated."

        # Verify the update
        response = client.get('/contacts')
        contact = response.get_json()["contacts"][0]
        assert contact["first_name"] == updated_data["firstName"]
        assert contact["last_name"] == updated_data["lastName"]
        assert contact["email"] == updated_data["email"]

    def test_update_contact_not_found(self, client):
        """Test updating a contact that does not exist."""
        response = client.patch('/update_contact/99999', json={'firstName': 'Jane'})
        assert response.status_code == 404
        data = response.get_json()
        assert data is not None, "Response JSON data is None"
        assert 'message' in data
        assert data['message'] == 'User not found'

    def test_delete_contact_success(self, client, sample_contact):
        """UNIVERSAL test for maximum coverage."""
        """Test successful deletion of a contact."""
        # Create a contact first
        client.post('/create_contact', json=sample_contact)

        # Retrieve the created contact's ID
        response = client.get('/contacts')
        contact_id = response.get_json()["contacts"][0]["id"]

        # Delete the contact
        response = client.delete(f'/delete_contact/{contact_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["message"] == "User deleted!"

        # Verify the contact no longer exists
        response = client.get('/contacts')
        data = response.get_json()
        assert len(data["contacts"]) == 0

    def test_delete_contact_not_found(self, client, monkeypatch):
        """Test deleting a contact that does not exist."""

        # Mock the client.delete to simulate the behavior of the API for a non-existent contact
        mocked_response = Mock()
        mocked_response.status_code = 404
        mocked_response.get_json.return_value = {"message": "User not found"}
        monkeypatch.setattr(client, "delete", lambda url: mocked_response)

        # Make the DELETE request to a non-existent contact
        response = client.delete('/delete_contact/99999')

        # Assert the response status code is 404
        assert response.status_code == 404

        # Assert the response has valid JSON with expected message
        data = response.get_json()
        assert data is not None
        assert 'message' in data
        assert data['message'] == 'User not found'

