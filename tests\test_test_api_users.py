```python
import pytest
from unittest.mock import MagicMock
from typing import Dict, Any

# Assuming the code to be tested is in a file named 'api.py'
from api import update_user, UserNotFoundError, InvalidUserDataError

# Define fixtures for test data
@pytest.fixture
def valid_user_data() -> Dict[str, Any]:
    """Fixture providing valid user data."""
    return {"name": "Updated Name", "email": "updated@example.com"}

@pytest.fixture
def invalid_user_data() -> Dict[str, Any]:
    """Fixture providing invalid user data (missing email)."""
    return {"name": "Updated Name"}

@pytest.fixture
def mock_user_db() -> MagicMock:
    """Fixture providing a mock user database."""
    mock_db = MagicMock()
    mock_db.get_user.return_value = {"id": 1, "name": "Original Name", "email": "original@example.com"}
    return mock_db

# Unit tests for update_user function
def test_update_user_success(mock_user_db: MagicMock, valid_user_data: Dict[str, Any]) -> None:
    """Test successful user update."""
    updated_user = update_user(1, valid_user_data, mock_user_db)
    assert updated_user["id"] == 1
    assert updated_user["name"] == "Updated Name"
    assert updated_user["email"] == "updated@example.com"
    mock_user_db.update_user.assert_called_once_with(1, valid_user_data)

def test_update_user_not_found(mock_user_db: MagicMock, valid_user_data: Dict[str, Any]) -> None:
    """Test user update when user is not found."""
    mock_user_db.get_user.return_value = None
    with pytest.raises(UserNotFoundError):
        update_user(1, valid_user_data, mock_user_db)
    mock_user_db.update_user.assert_not_called()

def test_update_user_invalid_data(mock_user_db: MagicMock, invalid_user_data: Dict[str, Any]) -> None:
    """Test user update with invalid data."""
    with pytest.raises(InvalidUserDataError):
        update_user(1, invalid_user_data, mock_user_db)
    mock_user_db.update_user.assert_not_called()

def test_update_user_empty_data(mock_user_db: MagicMock) -> None:
    """Test user update with empty data (no fields to update)."""
    with pytest.raises(InvalidUserDataError):
        update_user(1, {}, mock_user_db)
    mock_user_db.update_user.assert_not_called()

def test_update_user_partial_data(mock_user_db: MagicMock) -> None:
    """Test user update with partial data (only name)."""
    user_data = {"name": "Updated Name"}
    updated_user = update_user(1, user_data, mock_user_db)
    assert updated_user["id"] == 1
    assert updated_user["name"] == "Updated Name"
    assert updated_user["email"] == "original@example.com"  # Email should remain unchanged
    mock_user_db.update_user.assert_called_once_with(1, user_data)

def test_update_user_with_extra_fields(mock_user_db: MagicMock, valid_user_data: Dict[str, Any]) -> None:
    """Test user update with extra fields in the data."""
    user_data = {**valid_user_data, "extra_field": "extra_value"}
    updated_user = update_user(1, user_data, mock_user_db)
    assert updated_user["id"] == 1
    assert updated_user["name"] == "Updated Name"
    assert updated_user["email"] == "updated@example.com"
    mock_user_db.update_user.assert_called_once_with(1, valid_user_data)  # Only valid fields should be passed

# Integration tests (if applicable - depends on the actual implementation)
# Example:
# def test_update_user_integration(real_user_db, valid_user_data):
#     # Assuming real_user_db is a fixture that provides a real database connection
#     updated_user = update_user(1, valid_user_data, real_user_db)
#     assert updated_user["id"] == 1
#     assert updated_user["name"] == "Updated Name"
#     # ... other assertions
```