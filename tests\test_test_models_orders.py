```python
import pytest
from typing import List, Dict, Any
from unittest.mock import MagicMock

# Assuming the models_orders module is in the same directory as the tests
from models_orders import Order, OrderManager  # Replace with the actual module path


@pytest.fixture
def order_data() -> Dict[str, Any]:
    """Fixture to provide sample order data."""
    return {
        "order_id": "123",
        "customer_id": "456",
        "items": ["item1", "item2"],
        "total_amount": 100.0,
        "status": "pending",
    }


@pytest.fixture
def order(order_data: Dict[str, Any]) -> Order:
    """Fixture to create an Order instance."""
    return Order(**order_data)


@pytest.fixture
def order_manager() -> OrderManager:
    """Fixture to create an OrderManager instance."""
    return OrderManager()


class TestOrder:
    """Tests for the Order class."""

    def test_order_creation(self, order_data: Dict[str, Any]):
        """Test that an Order object is created correctly."""
        order = Order(**order_data)
        assert order.order_id == "123"
        assert order.customer_id == "456"
        assert order.items == ["item1", "item2"]
        assert order.total_amount == 100.0
        assert order.status == "pending"

    def test_order_representation(self, order: Order):
        """Test the string representation of an Order object."""
        expected_representation = (
            f"Order(order_id='{order.order_id}', customer_id='{order.customer_id}', "
            f"items={order.items}, total_amount={order.total_amount}, status='{order.status}')"
        )
        assert repr(order) == expected_representation

    def test_update_status(self, order: Order):
        """Test updating the status of an order."""
        order.update_status("shipped")
        assert order.status == "shipped"

    def test_add_item(self, order: Order):
        """Test adding an item to the order."""
        order.add_item("item3")
        assert "item3" in order.items

    def test_remove_item(self, order: Order):
        """Test removing an item from the order."""
        order.remove_item("item1")
        assert "item1" not in order.items
        assert "item2" in order.items

    def test_remove_nonexistent_item(self, order: Order):
        """Test removing a non-existent item from the order."""
        with pytest.raises(ValueError, match="Item 'nonexistent_item' not found in order."):
            order.remove_item("nonexistent_item")


class TestOrderManager:
    """Tests for the OrderManager class."""

    def test_add_order(self, order_manager: OrderManager, order: Order):
        """Test adding an order to the manager."""
        order_manager.add_order(order)
        assert order.order_id in order_manager.orders
        assert order_manager.orders[order.order_id] == order

    def test_get_order(self, order_manager: OrderManager, order: Order):
        """Test retrieving an order from the manager."""
        order_manager.add_order(order)
        retrieved_order = order_manager.get_order(order.order_id)
        assert retrieved_order == order

    def test_get_nonexistent_order(self, order_manager: OrderManager):
        """Test retrieving a non-existent order."""
        retrieved_order = order_manager.get_order("nonexistent_order_id")
        assert retrieved_order is None

    def test_list_orders_empty(self, order_manager: OrderManager):
        """Test listing orders when there are no orders."""
        assert order_manager.list_orders() == []

    def test_list_orders_multiple(self, order_manager: OrderManager, order: Order):
        """Test listing multiple orders."""
        order2_data = {
            "order_id": "456",
            "customer_id": "789",
            "items": ["item4", "item5"],
            "total_amount": 200.0,
            "status": "processing",
        }
        order2 = Order(**order2_data)

        order_manager.add_order(order)
        order_manager.add_order(order2)

        orders = order_manager.list_orders()
        assert len(orders) == 2
        assert order in orders
        assert order2 in orders

    def test_update_order(self, order_manager: OrderManager, order: Order):
        """Test updating an existing order."""
        order_manager.add_order(order)
        updated_data = {
            "customer_id": "999",
            "items": ["item1", "item3"],
            "total_amount": 150.0,
            "status": "shipped",
        }
        order_manager.update_order(order.order_id, updated_data)
        updated_order = order_manager.get_order(order.order_id)

        assert updated_order.customer_id == "999"
        assert updated_order.items == ["item1", "item3"]
        assert updated_order.total_amount == 150.0
        assert updated_order.status == "shipped"

    def test_update_nonexistent_order(self, order_manager: OrderManager):
        """Test updating a non-existent order."""
        with pytest.raises(ValueError, match="Order with ID 'nonexistent_order_id' not found."):
            order_manager.update_order("nonexistent_order_id", {"status": "shipped"})

    def test_delete_order(self, order_manager: OrderManager, order: Order):
        """Test deleting an order."""
        order_manager.add_order(order)
        order_manager.delete_order(order.order_id)
        assert order.order_id not in order_manager.orders
        assert order_manager.get_order(order.order_id) is None

    def test_delete_nonexistent_order(self, order_manager: OrderManager):
        """Test deleting a non-existent order."""
        with pytest.raises(ValueError, match="Order with ID 'nonexistent_order_id' not found."):
            order_manager.delete_order("nonexistent_order_id")
```