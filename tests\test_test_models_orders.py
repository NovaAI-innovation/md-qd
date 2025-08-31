```python
import pytest
from typing import List, Dict, Any
from unittest.mock import MagicMock

# Assuming the models and functions are in a file named 'app/models.py'
# and the order related functions are in 'app/models/orders.py'
from app.models.orders import Order, create_order, get_order, update_order, delete_order, list_orders  # Replace with your actual import path

# Define fixtures for common test objects
@pytest.fixture
def sample_order_data() -> Dict[str, Any]:
    """Fixture to provide sample order data."""
    return {
        "customer_id": 1,
        "items": [{"product_id": 101, "quantity": 2}],
        "total_amount": 100.0,
        "status": "pending"
    }

@pytest.fixture
def sample_order(sample_order_data: Dict[str, Any]) -> Order:
    """Fixture to create a sample Order object."""
    return Order(**sample_order_data)

@pytest.fixture
def mock_db_session():
    """Fixture to mock a database session."""
    # Create a mock session object.  Adjust as needed for your ORM.
    mock_session = MagicMock()
    return mock_session


# Unit tests for Order class
def test_order_creation(sample_order_data: Dict[str, Any]):
    """Test Order object creation."""
    order = Order(**sample_order_data)
    assert order.customer_id == sample_order_data["customer_id"]
    assert order.items == sample_order_data["items"]
    assert order.total_amount == sample_order_data["total_amount"]
    assert order.status == sample_order_data["status"]


# Unit tests for create_order function
def test_create_order(mock_db_session, sample_order_data: Dict[str, Any]):
    """Test creating an order."""
    new_order = create_order(mock_db_session, sample_order_data)
    assert new_order.customer_id == sample_order_data["customer_id"]
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_create_order_invalid_data(mock_db_session):
    """Test creating an order with invalid data."""
    with pytest.raises(TypeError):  # Or appropriate exception
        create_order(mock_db_session, {"invalid": "data"})


# Unit tests for get_order function
def test_get_order(mock_db_session, sample_order: Order):
    """Test getting an order by ID."""
    mock_db_session.query().get.return_value = sample_order
    retrieved_order = get_order(mock_db_session, 1)
    assert retrieved_order == sample_order
    mock_db_session.query().get.assert_called_once_with(1)


def test_get_order_not_found(mock_db_session):
    """Test getting an order that does not exist."""
    mock_db_session.query().get.return_value = None
    retrieved_order = get_order(mock_db_session, 999)
    assert retrieved_order is None


# Unit tests for update_order function
def test_update_order(mock_db_session, sample_order: Order):
    """Test updating an order."""
    mock_db_session.query().get.return_value = sample_order
    updated_data = {"status": "shipped"}
    updated_order = update_order(mock_db_session, 1, updated_data)
    assert updated_order.status == "shipped"
    mock_db_session.commit.assert_called_once()


def test_update_order_not_found(mock_db_session):
    """Test updating an order that does not exist."""
    mock_db_session.query().get.return_value = None
    updated_data = {"status": "shipped"}
    with pytest.raises(ValueError): # Or appropriate exception
        update_order(mock_db_session, 999, updated_data)


# Unit tests for delete_order function
def test_delete_order(mock_db_session, sample_order: Order):
    """Test deleting an order."""
    mock_db_session.query().get.return_value = sample_order
    delete_order(mock_db_session, 1)
    mock_db_session.delete.assert_called_once_with(sample_order)
    mock_db_session.commit.assert_called_once()


def test_delete_order_not_found(mock_db_session):
    """Test deleting an order that does not exist."""
    mock_db_session.query().get.return_value = None
    with pytest.raises(ValueError): # Or appropriate exception
        delete_order(mock_db_session, 999)


# Unit tests for list_orders function
def test_list_orders(mock_db_session, sample_order: Order):
    """Test listing orders."""
    mock_db_session.query().all.return_value = [sample_order]
    orders = list_orders(mock_db_session)
    assert len(orders) == 1
    assert orders[0] == sample_order
    mock_db_session.query().all.assert_called_once()


def test_list_orders_empty(mock_db_session):
    """Test listing orders when no orders exist."""
    mock_db_session.query().all.return_value = []
    orders = list_orders(mock_db_session)
    assert len(orders) == 0


# Integration tests (if applicable - requires a real database setup)
# Example:
# @pytest.mark.integration
# def test_create_and_get_order_integration(db_session, sample_order_data):
#     """Integration test for creating and retrieving an order."""
#     new_order = create_order(db_session, sample_order_data)
#     retrieved_order = get_order(db_session, new_order.id)
#     assert retrieved_order.customer_id == sample_order_data["customer_id"]
```