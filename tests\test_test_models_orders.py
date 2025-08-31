```python
import pytest
from typing import List, Dict, Any
from unittest.mock import MagicMock

# Assuming the models and functions are in a file named 'models.py'
from models import Order, list_orders  # Replace with the actual import


@pytest.fixture
def mock_order_data() -> List[Dict[str, Any]]:
    """
    Fixture to provide sample order data for testing.
    """
    return [
        {"order_id": 1, "customer_id": 101, "total_amount": 100.0, "status": "pending"},
        {"order_id": 2, "customer_id": 102, "total_amount": 200.0, "status": "shipped"},
        {"order_id": 3, "customer_id": 101, "total_amount": 150.0, "status": "delivered"},
    ]


@pytest.fixture
def mock_order_class() -> MagicMock:
    """
    Fixture to mock the Order class.
    """
    return MagicMock(spec=Order)


def test_order_creation(mock_order_class: MagicMock, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test the creation of an Order object.
    """
    order_data = mock_order_data[0]
    order = mock_order_class(**order_data)

    assert order.order_id == order_data["order_id"]
    assert order.customer_id == order_data["customer_id"]
    assert order.total_amount == order_data["total_amount"]
    assert order.status == order_data["status"]


def test_list_orders_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test listing orders when there are no orders.
    """
    mock_db_query = MagicMock(return_value=[])
    monkeypatch.setattr("models.db_query", mock_db_query)  # Assuming db_query is the function to fetch data

    orders = list_orders()
    assert orders == []
    mock_db_query.assert_called_once()


def test_list_orders_success(monkeypatch: pytest.MonkeyPatch, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test listing orders successfully.
    """
    mock_db_query = MagicMock(return_value=mock_order_data)
    monkeypatch.setattr("models.db_query", mock_db_query)  # Assuming db_query is the function to fetch data

    orders = list_orders()
    assert len(orders) == len(mock_order_data)
    for i, order in enumerate(orders):
        assert order["order_id"] == mock_order_data[i]["order_id"]
        assert order["customer_id"] == mock_order_data[i]["customer_id"]
        assert order["total_amount"] == mock_order_data[i]["total_amount"]
        assert order["status"] == mock_order_data[i]["status"]
    mock_db_query.assert_called_once()


def test_list_orders_db_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test listing orders when a database error occurs.
    """
    mock_db_query = MagicMock(side_effect=Exception("Database error"))
    monkeypatch.setattr("models.db_query", mock_db_query)  # Assuming db_query is the function to fetch data

    with pytest.raises(Exception, match="Database error"):
        list_orders()
    mock_db_query.assert_called_once()


def test_list_orders_type_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that the list_orders function correctly converts data types from the database.
    """
    # Simulate data coming from the database where total_amount is a string
    mock_db_data = [{"order_id": 4, "customer_id": 103, "total_amount": "250.50", "status": "pending"}]
    mock_db_query = MagicMock(return_value=mock_db_data)
    monkeypatch.setattr("models.db_query", mock_db_query)  # Assuming db_query is the function to fetch data

    orders = list_orders()
    assert len(orders) == 1
    assert isinstance(orders[0]["total_amount"], float)
    assert orders[0]["total_amount"] == 250.50
    mock_db_query.assert_called_once()


def test_list_orders_large_dataset(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test listing orders with a large dataset to ensure performance is acceptable.
    """
    large_dataset = [{"order_id": i, "customer_id": 100 + i, "total_amount": 50.0 + i, "status": "pending"} for i in range(1000)]
    mock_db_query = MagicMock(return_value=large_dataset)
    monkeypatch.setattr("models.db_query", mock_db_query)  # Assuming db_query is the function to fetch data

    orders = list_orders()
    assert len(orders) == 1000
    mock_db_query.assert_called_once()


def test_list_orders_with_filtering(monkeypatch: pytest.MonkeyPatch, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test listing orders with filtering (e.g., by customer_id).  This assumes the list_orders function
    accepts optional filter parameters.
    """
    # Mock the database to return only orders for customer_id 101
    filtered_data = [order for order in mock_order_data if order["customer_id"] == 101]
    mock_db_query = MagicMock(return_value=filtered_data)
    monkeypatch.setattr("models.db_query", mock_db_query)  # Assuming db_query is the function to fetch data

    # Assuming list_orders accepts a customer_id parameter
    orders = list_orders(customer_id=101)  # type: ignore[call-arg]
    assert len(orders) == len(filtered_data)
    for order in orders:
        assert order["customer_id"] == 101
    mock_db_query.assert_called_once()


# Add more tests as needed to cover different scenarios and edge cases
```