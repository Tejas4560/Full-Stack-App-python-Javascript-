"""Tests for models module."""

import sys
import os
import pytest
from models import Contact

sys.path.insert(0, r"/home/runner/work/Full-Stack-App-python-Javascript-/Full-Stack-App-python-Javascript-/pipeline/target_repo/backend")


class TestModelsUnit:
    """Unit tests for models."""

    @pytest.mark.parametrize(
        "id, first_name, last_name, email, expected_output",
        [
            (1, "John", "Doe", "john.doe@example.com", {"id": 1, "firstName": "John", "lastName": "Doe", "email": "john.doe@example.com"}),
            (2, "Jane", "Smith", "jane.smith@example.com", {"id": 2, "firstName": "Jane", "lastName": "Smith", "email": "jane.smith@example.com"}),
            (3, "Alice", "Johnson", "alice.johnson@example.com", {"id": 3, "firstName": "Alice", "lastName": "Johnson", "email": "alice.johnson@example.com"}),
        ],
    )
    def test_contact_to_json(self, id, first_name, last_name, email, expected_output):
        """UNIVERSAL test for maximum coverage."""
        contact = Contact(id=id, first_name=first_name, last_name=last_name, email=email)
        assert contact.to_json() == expected_output

    @pytest.mark.parametrize(
        "id, first_name, last_name, email",
        [
            (1, "John", "Doe", "john.doe@example.com"),
            (2, "Jane", "Smith", "jane.smith@example.com"),
            (3, "Alice", "Johnson", "alice.johnson@example.com"),
        ],
    )
    def test_contact_initialization(self, id, first_name, last_name, email):
        """UNIVERSAL test for maximum coverage."""
        contact = Contact(id=id, first_name=first_name, last_name=last_name, email=email)
        assert contact.id == id
        assert contact.first_name == first_name
        assert contact.last_name == last_name
        assert contact.email == email

    def test_contact_missing_required_fields(self):
        """UNIVERSAL test for maximum coverage."""
        with pytest.raises(TypeError):  # expecting a missing field error
            Contact(id=1, first_name="John")

        with pytest.raises(TypeError):  # expecting a missing field error
            Contact(id=1, last_name="Doe")

        with pytest.raises(TypeError):  # expecting a missing field error
            Contact(id=1, email="john.doe@example.com")

    def test_contact_str_representation(self):
        """UNIVERSAL test for maximum coverage."""
        contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")
        expected_output = f"<Contact {contact.id} - {contact.first_name} {contact.last_name}>"
        assert str(contact) == expected_output

