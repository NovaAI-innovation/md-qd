```python
import pytest
from unittest.mock import patch
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.users import User  # Assuming the path and class name
from app.schemas.users import UserCreate, UserUpdate  # Assuming the path and class name
from app.crud.users import create_user, get_user, get_user_by_email, get_users, update_user, delete_user  # Assuming the path and function names


@pytest.fixture
def mock_user_data() -> Dict[str, Any]:
    """Fixture to provide sample user data."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "is_active": True,
        "is_superuser": False,
    }


@pytest.fixture
def mock_user_create(mock_user_data: Dict[str, Any]) -> UserCreate:
    """Fixture to provide a UserCreate instance."""
    return UserCreate(**mock_user_data)


@pytest.fixture
def mock_user_update() -> UserUpdate:
    """Fixture to provide sample user update data."""
    return UserUpdate(first_name="Updated", last_name="User")


def test_create_user(db: Session, mock_user_create: UserCreate):
    """Test creating a new user."""
    user = create_user(db, mock_user_create)
    assert user.email == mock_user_create.email
    assert user.first_name == mock_user_create.first_name
    assert user.is_active == mock_user_create.is_active
    assert not user.hashed_password is None


def test_create_user_duplicate_email(db: Session, mock_user_create: UserCreate):
    """Test creating a user with a duplicate email."""
    create_user(db, mock_user_create)
    with pytest.raises(SQLAlchemyError):  # Assuming unique constraint raises this
        create_user(db, mock_user_create)
        db.rollback()  # Rollback to prevent database errors in subsequent tests


def test_get_user(db: Session, mock_user_create: UserCreate):
    """Test getting a user by ID."""
    user = create_user(db, mock_user_create)
    retrieved_user = get_user(db, user.id)
    assert retrieved_user == user


def test_get_user_not_found(db: Session):
    """Test getting a user that does not exist."""
    retrieved_user = get_user(db, 999)  # Assuming ID 999 does not exist
    assert retrieved_user is None


def test_get_user_by_email(db: Session, mock_user_create: UserCreate):
    """Test getting a user by email."""
    user = create_user(db, mock_user_create)
    retrieved_user = get_user_by_email(db, mock_user_create.email)
    assert retrieved_user == user


def test_get_user_by_email_not_found(db: Session):
    """Test getting a user by email that does not exist."""
    retrieved_user = get_user_by_email(db, "nonexistent@example.com")
    assert retrieved_user is None


def test_get_users(db: Session, mock_user_create: UserCreate):
    """Test getting all users."""
    user1 = create_user(db, mock_user_create)
    mock_user_create2 = UserCreate(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        password="password456",
        is_active=True,
        is_superuser=False,
    )
    user2 = create_user(db, mock_user_create2)

    users = get_users(db, skip=0, limit=10)
    assert len(users) >= 2
    assert user1 in users
    assert user2 in users


def test_get_users_pagination(db: Session, mock_user_create: UserCreate):
    """Test getting users with pagination."""
    for i in range(5):
        mock_user_create_i = UserCreate(
            first_name=f"User{i}",
            last_name="Doe",
            email=f"user{i}@example.com",
            password="password",
            is_active=True,
            is_superuser=False,
        )
        create_user(db, mock_user_create_i)

    users = get_users(db, skip=1, limit=2)
    assert len(users) == 2
    emails = [user.email for user in users]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


def test_update_user(db: Session, mock_user_create: UserCreate, mock_user_update: UserUpdate):
    """Test updating an existing user."""
    user = create_user(db, mock_user_create)
    updated_user = update_user(db, user.id, mock_user_update)

    assert updated_user is not None
    assert updated_user.first_name == mock_user_update.first_name
    assert updated_user.last_name == mock_user_update.last_name
    assert updated_user.email == user.email  # Email should not be updated
    assert updated_user.id == user.id


def test_update_user_not_found(db: Session, mock_user_update: UserUpdate):
    """Test updating a user that does not exist."""
    updated_user = update_user(db, 999, mock_user_update)  # Assuming ID 999 does not exist
    assert updated_user is None


def test_delete_user(db: Session, mock_user_create: UserCreate):
    """Test deleting a user."""
    user = create_user(db, mock_user_create)
    deleted = delete_user(db, user.id)
    assert deleted is True
    assert get_user(db, user.id) is None


def test_delete_user_not_found(db: Session):
    """Test deleting a user that does not exist."""
    deleted = delete_user(db, 999)  # Assuming ID 999 does not exist
    assert deleted is False
```