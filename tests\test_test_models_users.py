```python
import pytest
from unittest.mock import patch
from typing import Dict, Any
from models.users import User, UserUpdate

# Fixtures
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
def mock_user(mock_user_data: Dict[str, Any]) -> User:
    """Fixture to create a User instance."""
    return User(**mock_user_data)

@pytest.fixture
def mock_user_update_data() -> Dict[str, Any]:
    """Fixture to provide sample user update data."""
    return {
        "full_name": "Updated User Name",
        "disabled": True,
    }

@pytest.fixture
def mock_user_update(mock_user_update_data: Dict[str, Any]) -> UserUpdate:
    """Fixture to create a UserUpdate instance."""
    return UserUpdate(**mock_user_update_data)


# Unit Tests for User Model
def test_user_creation(mock_user_data: Dict[str, Any]) -> None:
    """Test User object creation."""
    user = User(**mock_user_data)
    assert user.user_id == 1
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.disabled is False


def test_user_representation(mock_user: User) -> None:
    """Test the string representation of the User object."""
    expected_representation = "User(user_id=1, username='testuser', email='test@example.com', full_name='Test User', disabled=False)"
    assert repr(mock_user) == expected_representation


# Unit Tests for UserUpdate Model
def test_user_update_creation(mock_user_update_data: Dict[str, Any]) -> None:
    """Test UserUpdate object creation."""
    user_update = UserUpdate(**mock_user_update_data)
    assert user_update.full_name == "Updated User Name"
    assert user_update.disabled is True


def test_user_update_representation(mock_user_update: UserUpdate) -> None:
    """Test the string representation of the UserUpdate object."""
    expected_representation = "UserUpdate(full_name='Updated User Name', disabled=True)"
    assert repr(mock_user_update) == expected_representation


def test_user_update_none_values() -> None:
    """Test UserUpdate with None values."""
    user_update = UserUpdate(full_name=None, disabled=None)
    assert user_update.full_name is None
    assert user_update.disabled is None


def test_user_update_empty_values() -> None:
    """Test UserUpdate with empty string values."""
    user_update = UserUpdate(full_name="", disabled=False)
    assert user_update.full_name == ""
    assert user_update.disabled is False


def test_user_update_partial_update() -> None:
    """Test UserUpdate with only one field updated."""
    user_update = UserUpdate(full_name="Partial Update")
    assert user_update.full_name == "Partial Update"
    assert user_update.disabled is None


# Integration Tests (Illustrative - Adapt to your actual integration points)
@pytest.mark.integration
def test_user_update_integration(mock_user: User, mock_user_update: UserUpdate) -> None:
    """Illustrative integration test: Simulating updating a user."""
    # This is a placeholder; adapt to your actual integration with database/service
    original_full_name = mock_user.full_name
    original_disabled = mock_user.disabled

    if mock_user_update.full_name is not None:
        mock_user.full_name = mock_user_update.full_name
    if mock_user_update.disabled is not None:
        mock_user.disabled = mock_user_update.disabled

    assert mock_user.full_name == mock_user_update.full_name
    assert mock_user.disabled == mock_user_update.disabled

    # Revert changes for cleanup (if needed in your actual integration)
    mock_user.full_name = original_full_name
    mock_user.disabled = original_disabled
```