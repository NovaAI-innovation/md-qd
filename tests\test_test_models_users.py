```python
import pytest
from unittest.mock import patch
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.users import User  # Assuming your User model is in this location
from app.schemas.users import UserCreate, UserUpdate  # Assuming your schemas are in this location
from app.crud.users import create_user, get_user, update_user, delete_user, get_user_by_email  # Assuming your CRUD functions are in this location


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
def mock_user_update_data() -> Dict[str, Any]:
    """Fixture to provide sample user update data."""
    return {
        "first_name": "Jane",
        "last_name": "Smith",
        "is_active": False,
    }


@pytest.fixture
def mock_user_update(mock_user_update_data: Dict[str, Any]) -> UserUpdate:
    """Fixture to provide a UserUpdate instance."""
    return UserUpdate(**mock_user_update_data)


def test_create_user(db: Session, mock_user_create: UserCreate):
    """Test creating a new user."""
    user = create_user(db, mock_user_create)
    assert user.first_name == mock_user_create.first_name
    assert user.email == mock_user_create.email
    assert user.is_active == mock_user_create.is_active
    assert not user.hashed_password == mock_user_create.password  # Check password hashing
    assert get_user(db, user.id) == user


def test_create_user_duplicate_email(db: Session, mock_user_create: UserCreate):
    """Test creating a user with an existing email."""
    create_user(db, mock_user_create)
    with pytest.raises(SQLAlchemyError):  # Expecting unique constraint violation
        create_user(db, mock_user_create)
    db.rollback()  # Rollback to prevent the duplicate entry from affecting other tests


def test_get_user(db: Session, mock_user_create: UserCreate):
    """Test getting a user by ID."""
    user = create_user(db, mock_user_create)
    retrieved_user = get_user(db, user.id)
    assert retrieved_user == user


def test_get_user_not_found(db: Session):
    """Test getting a user that does not exist."""
    retrieved_user = get_user(db, 999)  # Assuming 999 is a non-existent ID
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


def test_update_user(db: Session, mock_user_create: UserCreate, mock_user_update: UserUpdate):
    """Test updating an existing user."""
    user = create_user(db, mock_user_create)
    updated_user = update_user(db, user.id, mock_user_update)

    assert updated_user is not None
    assert updated_user.id == user.id
    assert updated_user.first_name == mock_user_update.first_name
    assert updated_user.last_name == mock_user_update.last_name
    assert updated_user.is_active == mock_user_update.is_active
    assert updated_user.email == user.email  # Email should not be changed
    assert get_user(db, user.id) == updated_user


def test_update_user_not_found(db: Session, mock_user_update: UserUpdate):
    """Test updating a user that does not exist."""
    updated_user = update_user(db, 999, mock_user_update)  # Assuming 999 is a non-existent ID
    assert updated_user is None


def test_update_user_invalid_data(db: Session, mock_user_create: UserCreate):
    """Test updating a user with invalid data (e.g., empty first name)."""
    user = create_user(db, mock_user_create)
    with pytest.raises(ValueError):
        update_user(db, user.id, UserUpdate(first_name=""))  # type: ignore
    db.rollback()


def test_delete_user(db: Session, mock_user_create: UserCreate):
    """Test deleting a user."""
    user = create_user(db, mock_user_create)
    deleted = delete_user(db, user.id)
    assert deleted is True
    assert get_user(db, user.id) is None


def test_delete_user_not_found(db: Session):
    """Test deleting a user that does not exist."""
    deleted = delete_user(db, 999)  # Assuming 999 is a non-existent ID
    assert deleted is False


def test_update_user_email(db: Session, mock_user_create: UserCreate):
    """Test updating a user's email."""
    user = create_user(db, mock_user_create)
    new_email = "new.email@example.com"
    user_update = UserUpdate(email=new_email)
    updated_user = update_user(db, user.id, user_update)
    assert updated_user is not None
    assert updated_user.email == new_email
    assert get_user(db, user.id).email == new_email


def test_update_user_email_duplicate(db: Session, mock_user_create: UserCreate):
    """Test updating a user's email to an existing email."""
    existing_user = create_user(db, mock_user_create)
    new_user_data = {
        "first_name": "Another",
        "last_name": "User",
        "email": "another.user@example.com",
        "password": "password123",
        "is_active": True,
        "is_superuser": False,
    }
    new_user_create = UserCreate(**new_user_data)
    new_user = create_user(db, new_user_create)

    with pytest.raises(SQLAlchemyError):
        update_user(db, new_user.id, UserUpdate(email=existing_user.email))
    db.rollback()
```