```python
import pytest
from unittest.mock import MagicMock
from typing import Dict, Any

# Assuming the existence of a Flask app and User model
# Replace with your actual imports
from your_app import app, User  # type: ignore
from your_app import db  # type: ignore


@pytest.fixture
def client():
    """
    Pytest fixture that returns a Flask test client.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
            yield client
            db.drop_all()  # Drop tables after test


@pytest.fixture
def new_user() -> Dict[str, Any]:
    """
    Pytest fixture that returns a dictionary representing a new user.
    """
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }


def test_update_user_success(client, new_user):
    """
    Test case for successfully updating a user.
    """
    # Create a user first
    with app.app_context():
        user = User(username=new_user['username'], email=new_user['email'])
        user.set_password(new_user['password'])
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Update the user
    update_data = {'username': 'updateduser', 'email': 'updated@example.com'}
    response = client.put(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'updateduser'
    assert data['email'] == 'updated@example.com'

    # Verify the update in the database
    with app.app_context():
        updated_user = User.query.get(user_id)
        assert updated_user.username == 'updateduser'
        assert updated_user.email == 'updated@example.com'


def test_update_user_not_found(client):
    """
    Test case for attempting to update a user that does not exist.
    """
    response = client.put('/users/999', json={'username': 'test'})
    assert response.status_code == 404
    data = response.get_json()
    assert 'User not found' in data['message']


def test_update_user_invalid_data(client, new_user):
    """
    Test case for attempting to update a user with invalid data.
    """
    # Create a user first
    with app.app_context():
        user = User(username=new_user['username'], email=new_user['email'])
        user.set_password(new_user['password'])
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Attempt to update with invalid data (e.g., missing username)
    response = client.put(f'/users/{user_id}', json={'email': 'updated@example.com'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'username' in data['message']  # Adjust based on your validation logic


def test_update_user_empty_data(client, new_user):
    """
    Test case for attempting to update a user with empty data.
    """
    # Create a user first
    with app.app_context():
        user = User(username=new_user['username'], email=new_user['email'])
        user.set_password(new_user['password'])
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Attempt to update with empty data
    response = client.put(f'/users/{user_id}', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'No update data provided' in data['message']  # Adjust based on your validation logic


def test_update_user_duplicate_username(client, new_user):
    """
    Test case for attempting to update a user with a duplicate username.
    """
    # Create two users
    with app.app_context():
        user1 = User(username=new_user['username'], email=new_user['email'])
        user1.set_password(new_user['password'])
        db.session.add(user1)
        db.session.commit()
        user1_id = user1.id

        user2 = User(username='anotheruser', email='another@example.com')
        user2.set_password('anotherpassword')
        db.session.add(user2)
        db.session.commit()

    # Attempt to update user1 with user2's username
    update_data = {'username': 'anotheruser'}
    response = client.put(f'/users/{user1_id}', json=update_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'Username already exists' in data['message']  # Adjust based on your validation logic


def test_update_user_duplicate_email(client, new_user):
    """
    Test case for attempting to update a user with a duplicate email.
    """
    # Create two users
    with app.app_context():
        user1 = User(username=new_user['username'], email=new_user['email'])
        user1.set_password(new_user['password'])
        db.session.add(user1)
        db.session.commit()
        user1_id = user1.id

        user2 = User(username='anotheruser', email='another@example.com')
        user2.set_password('anotherpassword')
        db.session.add(user2)
        db.session.commit()

    # Attempt to update user1 with user2's email
    update_data = {'email': 'another@example.com'}
    response = client.put(f'/users/{user1_id}', json=update_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'Email already exists' in data['message']  # Adjust based on your validation logic


def test_update_user_with_password_change(client, new_user):
    """
    Test case for updating a user and changing the password.
    """
    # Create a user first
    with app.app_context():
        user = User(username=new_user['username'], email=new_user['email'])
        user.set_password(new_user['password'])
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Update the user with a new password
    update_data = {'password': 'newpassword'}
    response = client.put(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200

    # Verify the password update in the database
    with app.app_context():
        updated_user = User.query.get(user_id)
        assert updated_user.check_password('newpassword')  # Assuming check_password method exists


def test_update_user_with_partial_data(client, new_user):
    """
    Test case for updating a user with only partial data (e.g., only username).
    """
    # Create a user first
    with app.app_context():
        user = User(username=new_user['username'], email=new_user['email'])
        user.set_password(new_user['password'])
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Update the user with only the username
    update_data = {'username': 'updateduser'}
    response = client.put(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'updateduser'
    assert data['email