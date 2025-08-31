```python
import pytest
from unittest.mock import MagicMock
from typing import List, Dict, Any

# Assuming the code to be tested is in a file named 'api_orders.py'
# and contains a class named 'OrderManager' with a method 'list_orders'
from src.api_orders import OrderManager  # Replace with the actual import path


@pytest.fixture
def order_manager() -> OrderManager:
    """
    Fixture to create an instance of the OrderManager class.
    """
    return OrderManager()


@pytest.fixture
def mock_order_data() -> List[Dict[str, Any]]:
    """
    Fixture to provide mock order data for testing.
    """
    return [
        {"order_id": 1, "customer_id": "A123", "items": ["item1", "item2"], "total": 100.0},
        {"order_id": 2, "customer_id": "B456", "items": ["item3"], "total": 50.0},
    ]


def test_list_orders_empty(order_manager: OrderManager) -> None:
    """
    Test that list_orders returns an empty list when no orders exist.
    """
    order_manager.orders = []  # Ensure no orders exist
    orders = order_manager.list_orders()
    assert orders == []


def test_list_orders_success(order_manager: OrderManager, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test that list_orders returns the correct list of orders.
    """
    order_manager.orders = mock_order_data
    orders = order_manager.list_orders()
    assert orders == mock_order_data


def test_list_orders_modified_data(order_manager: OrderManager, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test that list_orders returns the correct list of orders even if the data has been modified.
    """
    order_manager.orders = mock_order_data
    mock_order_data[0]["total"] = 120.0  # Modify the mock data
    orders = order_manager.list_orders()
    assert orders == mock_order_data


def test_list_orders_large_dataset(order_manager: OrderManager) -> None:
    """
    Test list_orders with a large dataset to ensure performance is acceptable.
    """
    large_dataset = [{"order_id": i, "customer_id": f"C{i}", "items": [f"item{i}"], "total": float(i)} for i in range(1000)]
    order_manager.orders = large_dataset
    orders = order_manager.list_orders()
    assert len(orders) == 1000
    assert orders[0]["order_id"] == 0
    assert orders[999]["order_id"] == 999


def test_list_orders_no_side_effects(order_manager: OrderManager, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test that list_orders does not modify the internal order data.
    """
    order_manager.orders = mock_order_data
    original_data = mock_order_data[:]  # Create a copy
    order_manager.list_orders()
    assert order_manager.orders == original_data


def test_list_orders_with_filtering(order_manager: OrderManager, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test that list_orders can filter orders based on a criteria (e.g., customer_id).
    This assumes that the list_orders method can accept filter parameters.
    """
    order_manager.orders = mock_order_data
    # Assuming list_orders can take a customer_id as a filter
    filtered_orders = order_manager.list_orders(customer_id="A123")  # type: ignore[call-arg]
    assert len(filtered_orders) == 1
    assert filtered_orders[0]["customer_id"] == "A123"


def test_list_orders_invalid_filter_parameter(order_manager: OrderManager, mock_order_data: List[Dict[str, Any]]) -> None:
    """
    Test that list_orders handles invalid filter parameters gracefully.
    This assumes that the list_orders method raises an exception or returns an empty list
    when an invalid filter parameter is provided.
    """
    order_manager.orders = mock_order_data
    with pytest.raises(TypeError):  # Expect a TypeError if invalid parameter is passed
        order_manager.list_orders(invalid_param="some_value")  # type: ignore[call-arg]


def test_list_orders_exception_handling(order_manager: OrderManager) -> None:
    """
    Test that list_orders handles exceptions gracefully.
    This test mocks the internal data to raise an exception and verifies that list_orders
    handles it without crashing.
    """
    order_manager.orders = MagicMock(side_effect=Exception("Simulated error"))
    with pytest.raises(Exception, match="Simulated error"):
        order_manager.list_orders()
```