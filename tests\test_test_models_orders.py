```python
import pytest
from unittest.mock import patch
from typing import List, Dict, Any
from models.orders import Order, OrderItem  # Assuming models/orders.py exists

# Fixtures
@pytest.fixture
def sample_order_item() -> OrderItem:
    """Fixture for creating a sample OrderItem."""
    return OrderItem(product_id=1, quantity=2, price=10.0)

@pytest.fixture
def sample_order(sample_order_item: OrderItem) -> Order:
    """Fixture for creating a sample Order."""
    return Order(order_id=1, customer_id=101, items=[sample_order_item])

# Unit Tests for OrderItem
def test_order_item_creation(sample_order_item: OrderItem) -> None:
    """Test OrderItem creation."""
    assert sample_order_item.product_id == 1
    assert sample_order_item.quantity == 2
    assert sample_order_item.price == 10.0

def test_order_item_total(sample_order_item: OrderItem) -> None:
    """Test OrderItem total calculation."""
    assert sample_order_item.total() == 20.0

# Unit Tests for Order
def test_order_creation(sample_order: Order) -> None:
    """Test Order creation."""
    assert sample_order.order_id == 1
    assert sample_order.customer_id == 101
    assert len(sample_order.items) == 1

def test_order_add_item(sample_order: Order) -> None:
    """Test adding an item to an Order."""
    new_item = OrderItem(product_id=2, quantity=1, price=5.0)
    sample_order.add_item(new_item)
    assert len(sample_order.items) == 2
    assert sample_order.items[1].product_id == 2

def test_order_remove_item(sample_order: Order, sample_order_item: OrderItem) -> None:
    """Test removing an item from an Order."""
    sample_order.remove_item(sample_order_item)
    assert len(sample_order.items) == 0

def test_order_remove_nonexistent_item(sample_order: Order) -> None:
    """Test removing a non-existent item from an Order."""
    nonexistent_item = OrderItem(product_id=999, quantity=1, price=1.0)
    with pytest.raises(ValueError):
        sample_order.remove_item(nonexistent_item)

def test_order_total(sample_order: Order) -> None:
    """Test Order total calculation."""
    assert sample_order.total() == 20.0

    new_item = OrderItem(product_id=2, quantity=1, price=5.0)
    sample_order.add_item(new_item)
    assert sample_order.total() == 25.0

# Mocking and Patching Example (Illustrative - adapt to your actual implementation)
@patch("models.orders.Order.total")  # Assuming Order.total exists
def test_order_total_mocked(mock_total: Any, sample_order: Order) -> None:
    """Test Order total with a mocked total function."""
    mock_total.return_value = 100.0
    assert sample_order.total() == 100.0
    mock_total.assert_called_once()

# Integration Tests (Illustrative - adapt to your actual implementation)
# These tests would typically involve interacting with a database or external service.
# Example:
# @pytest.mark.integration
# def test_order_persistence(sample_order: Order) -> None:
#     """Test Order persistence to a database."""
#     # Assuming you have a function to save the order to the database
#     save_order(sample_order)
#     retrieved_order = get_order(sample_order.order_id)
#     assert retrieved_order == sample_order

# Example LIST operation tests (Adapt to your actual implementation)
# Assuming you have a function to list orders
# def test_list_orders() -> None:
#     """Test listing orders."""
#     orders = list_orders() # Assuming list_orders() function exists
#     assert isinstance(orders, list)
#     # Add more specific assertions based on your data and expected behavior

# def test_list_orders_empty() -> None:
#     """Test listing orders when there are no orders."""
#     # Assuming you can clear the orders before this test
#     clear_orders() # Assuming clear_orders() function exists
#     orders = list_orders()
#     assert orders == []

# def test_list_orders_with_filter() -> None:
#     """Test listing orders with a filter (e.g., by customer_id)."""
#     # Assuming you have a function to list orders with a filter
#     orders = list_orders(customer_id=101) # Assuming list_orders() can take filters
#     assert isinstance(orders, list)
#     # Add more specific assertions based on your data and expected behavior
#     for order in orders:
#         assert order.customer_id == 101
```