```python
import pytest
from unittest.mock import patch
from typing import Dict, Any

# Assuming the models and database setup are in these files
from src.models.users import User, create_user, get_user_by_id, get_user_by_email, update_user, delete_user
from src.db import get_db  # type: ignore

# Mock database session for testing
@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mock database session.
    """
    class MockSession:
        def __init__(self):
            self.data = {}
            self.next_id = 1

        def add(self, obj):
            if not hasattr(obj, 'id'):
                obj.id = self.next_id
                self.next_id += 1
            self.data[obj.id] = obj

        def commit(self):
            pass

        def rollback(self):
            pass

        def query(self, model):
            class MockQuery:
                def __init__(self, data):
                    self.data = data
                    self.model = model

                def filter(self, *args, **kwargs):
                    # Simplified filter logic for testing
                    filtered_data = self.data.values()
                    for arg in args:
                        if hasattr(arg, 'left') and hasattr(arg, 'right') and hasattr(arg, 'op'):
                            if arg.op == '==':
                                filtered_data = [item for item in filtered_data if getattr(item, arg.left.name) == arg.right.value]
                    return MockQuery(filtered_data)

                def first(self):
                    if self.data:
                        return list(self.data)[0]
                    return None

                def all(self):
                    return list(self.data.values())

                def delete(self):
                    for item_id in list(self.data.keys()):
                        del self.data[item_id]

            return MockQuery(self.data)

        def close(self):
            pass

    session = MockSession()
    with patch("src.db.get_db") as mock_get_db:
        mock_get_db.return_value = session
        yield session

# Test cases for User model and related functions
def test_create_user(mock_db_session: Any):
    """
    Test case for creating a new user.
    """
    user_data = {"email": "test@example.com", "password": "password123", "username": "testuser"}
    user = create_user(**user_data)
    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.username == "testuser"

def test_get_user_by_id(mock_db_session: Any):
    """
    Test case for retrieving a user by ID.
    """
    user_data = {"email": "test@example.com", "password": "password123", "username": "testuser"}
    user = create_user(**user_data)
    retrieved_user = get_user_by_id(user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"

def test_get_user_by_id_not_found(mock_db_session: Any):
    """
    Test case for retrieving a user by ID when the user does not exist.
    """
    retrieved_user = get_user_by_id(999)
    assert retrieved_user is None

def test_get_user_by_email(mock_db_session: Any):
    """
    Test case for retrieving a user by email.
    """
    user_data = {"email": "test@example.com", "password": "password123", "username": "testuser"}
    create_user(**user_data)
    retrieved_user = get_user_by_email("test@example.com")
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

def test_get_user_by_email_not_found(mock_db_session: Any):
    """
    Test case for retrieving a user by email when the user does not exist.
    """
    retrieved_user = get_user_by_email("nonexistent@example.com")
    assert retrieved_user is None

def test_update_user(mock_db_session: Any):
    """
    Test case for updating an existing user.
    """
    user_data = {"email": "test@example.com", "password": "password123", "username": "testuser"}
    user = create_user(**user_data)
    update_data = {"username": "newusername", "email": "newemail@example.com"}
    updated_user = update_user(user.id, **update_data)
    assert updated_user is not None
    assert updated_user.username == "newusername"
    assert updated_user.email == "newemail@example.com"

def test_update_user_not_found(mock_db_session: Any):
    """
    Test case for updating a user that does not exist.
    """
    update_data = {"username": "newusername", "email": "newemail@example.com"}
    updated_user = update_user(999, **update_data)
    assert updated_user is None

def test_update_user_partial_update(mock_db_session: Any):
    """
    Test case for partially updating a user.
    """
    user_data = {"email": "test@example.com", "password": "password123", "username": "testuser"}
    user = create_user(**user_data)
    update_data = {"username": "newusername"}
    updated_user = update_user(user.id, **update_data)
    assert updated_user is not None
    assert updated_user.username == "newusername"
    assert updated_user.email == "test@example.com"  # Email should remain unchanged

def test_delete_user(mock_db_session: Any):
    """
    Test case for deleting a user.
    """
    user_data = {"email": "test@example.com", "password": "password123", "username": "testuser"}
    user = create_user(**user_data)
    delete_user(user.id)
    retrieved_user = get_user_by_id(user.id)
    assert retrieved_user is None

def test_delete_user_not_found(mock_db_session: Any):
    """
    Test case for deleting a user that does not exist.
    """
    delete_user(999)  # Should not raise an error
    assert get_user_by_id(999) is None
```