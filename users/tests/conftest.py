import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    """Create a user which should automatically create UserData via signal"""
    return User.objects.create_user(username="testuser", email="testuser@example.com")
