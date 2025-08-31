```python
import pytest
from typing import List, Dict, Any
from unittest.mock import MagicMock

# Assuming the models.orders module is in the same directory as the tests
from models.orders import Order, OrderItem, OrderStatus  # type: ignore


@pytest.fixture
def sample_order_data() -> Dict[str, Any]:
    """Fixture providing sample order data."""
    return {
        "order_id": 1,
        "customer_id": 101,
        "order_date": "2023-10-26",
        "status": OrderStatus.PENDING,
        "items": [
            {"product_id": 1, "quantity": 2, "price": 10.0},
            {"product_id": 2, "quantity": 1, "price": 20.0},
        ],
    }


@pytest.fixture
def sample_order(sample_order_data: Dict[str, Any]) -> Order:
    """Fixture providing a sample Order object."""
    return Order(**sample_order_data)


def test_order_creation(sample_order_data: Dict[str, Any]) -> None:
    """Test Order object creation."""
    order = Order(**sample_order_data)
    assert order.order_id == sample_order_data["order_id"]
    assert order.customer_id == sample_order_data["customer_id"]
    assert order.order_date == sample_order_data["order_date"]
    assert order.status == sample_order_data["status"]
    assert len(order.items) == len(sample_order_data["items"])


def test_order_item_creation() -> None:
    """Test OrderItem object creation."""
    item_data = {"product_id": 1, "quantity": 2, "price": 10.0}
    item = OrderItem(**item_data)
    assert item.product_id == item_data["product_id"]
    assert item.quantity == item_data["quantity"]
    assert item.price == item_data["price"]


def test_order_total(sample_order: Order) -> None:
    """Test Order.total() method."""
    expected_total = sum(item.quantity * item.price for item in sample_order.items)
    assert sample_order.total() == expected_total


def test_order_status_enum() -> None:
    """Test OrderStatus enum values."""
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.SHIPPED.value == "shipped"
    assert OrderStatus.DELIVERED.value == "delivered"
    assert OrderStatus.CANCELLED.value == "cancelled"


def test_order_status_update(sample_order: Order) -> None:
    """Test Order.update_status() method."""
    sample_order.update_status(OrderStatus.SHIPPED)
    assert sample_order.status == OrderStatus.SHIPPED


def test_order_add_item(sample_order: Order) -> None:
    """Test Order.add_item() method."""
    new_item = OrderItem(product_id=3, quantity=3, price=5.0)
    sample_order.add_item(new_item)
    assert len(sample_order.items) == 3
    assert sample_order.items[-1] == new_item


def test_order_remove_item(sample_order: Order) -> None:
    """Test Order.remove_item() method."""
    initial_item_count = len(sample_order.items)
    item_to_remove = sample_order.items[0]
    sample_order.remove_item(item_to_remove)
    assert len(sample_order.items) == initial_item_count - 1
    assert item_to_remove not in sample_order.items


def test_order_remove_nonexistent_item(sample_order: Order) -> None:
    """Test Order.remove_item() with a non-existent item."""
    nonexistent_item = OrderItem(product_id=999, quantity=1, price=1.0)
    initial_item_count = len(sample_order.items)
    sample_order.remove_item(nonexistent_item)
    assert len(sample_order.items) == initial_item_count  # No change


def test_order_empty_items() -> None:
    """Test Order with no items."""
    order = Order(order_id=2, customer_id=102, order_date="2023-10-27", status=OrderStatus.PENDING, items=[])
    assert order.total() == 0.0


def test_order_invalid_status() -> None:
    """Test Order creation with invalid status."""
    with pytest.raises(ValueError):
        Order(order_id=3, customer_id=103, order_date="2023-10-28", status="invalid_status", items=[])  # type: ignore


def test_order_item_negative_quantity() -> None:
    """Test OrderItem creation with negative quantity."""
    with pytest.raises(ValueError):
        OrderItem(product_id=4, quantity=-1, price=10.0)


def test_order_item_negative_price() -> None:
    """Test OrderItem creation with negative price."""
    with pytest.raises(ValueError):
        OrderItem(product_id=5, quantity=1, price=-10.0)


def test_order_item_zero_quantity() -> None:
    """Test OrderItem creation with zero quantity."""
    item = OrderItem(product_id=6, quantity=0, price=10.0)
    assert item.quantity == 0


def test_order_item_zero_price() -> None:
    """Test OrderItem creation with zero price."""
    item = OrderItem(product_id=7, quantity=1, price=0.0)
    assert item.price == 0.0


def test_order_str_representation(sample_order: Order) -> None:
    """Test the string representation of the Order object."""
    assert str(sample_order) == f"Order ID: {sample_order.order_id}, Customer ID: {sample_order.customer_id}, Status: {sample_order.status}"


def test_order_item_str_representation() -> None:
    """Test the string representation of the OrderItem object."""
    item = OrderItem(product_id=8, quantity=4, price=7.5)
    assert str(item) == f"Product ID: {item.product_id}, Quantity: {item.quantity}, Price: {item.price}"
```