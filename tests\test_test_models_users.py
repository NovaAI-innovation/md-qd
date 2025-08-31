```python
import pytest
from unittest.mock import patch
from typing import Dict, Any

# Assuming the models_users module is in the same directory as tests
from .. import models_users
from ..models_users import User, UserUpdate


@pytest.fixture
def mock_user_data() -> Dict[str, Any]:
    """Fixture to provide sample user data."""
    return {
        "user_id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "disabled": False,
    }


@pytest.fixture
def mock_user_update_data() -> Dict[str, Any]:
    """Fixture to provide sample user update data."""
    return {
        "full_name": "Updated User Name",
        "disabled": True,
    }


def test_user_creation(mock_user_data: Dict[str, Any]) -> None:
    """Test the creation of a User object."""
    user = User(**mock_user_data)
    assert user.user_id == mock_user_data["user_id"]
    assert user.username == mock_user_data["username"]
    assert user.email == mock_user_data["email"]
    assert user.full_name == mock_user_data["full_name"]
    assert user.disabled == mock_user_data["disabled"]


def test_user_update_creation(mock_user_update_data: Dict[str, Any]) -> None:
    """Test the creation of a UserUpdate object."""
    user_update = UserUpdate(**mock_user_update_data)
    assert user_update.full_name == mock_user_update_data["full_name"]
    assert user_update.disabled == mock_user_update_data["disabled"]


def test_user_update_optional_fields() -> None:
    """Test UserUpdate with only some fields provided."""
    user_update = UserUpdate(full_name="Only Full Name")
    assert user_update.full_name == "Only Full Name"
    assert user_update.disabled is None


def test_user_update_empty() -> None:
    """Test UserUpdate with no fields provided."""
    user_update = UserUpdate()
    assert user_update.full_name is None
    assert user_update.disabled is None


def test_user_model_str(mock_user_data: Dict[str, Any]) -> None:
    """Test the string representation of the User model."""
    user = User(**mock_user_data)
    expected_str = f"User(user_id={user.user_id}, username='{user.username}', email='{user.email}', full_name='{user.full_name}', disabled={user.disabled})"
    assert str(user) == expected_str


def test_user_update_model_str(mock_user_update_data: Dict[str, Any]) -> None:
    """Test the string representation of the UserUpdate model."""
    user_update = UserUpdate(**mock_user_update_data)
    expected_str = f"UserUpdate(full_name='{user_update.full_name}', disabled={user_update.disabled})"
    assert str(user_update) == expected_str
```