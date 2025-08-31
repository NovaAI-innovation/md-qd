```python
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

# Example Order model (replace with your actual model)
class Order(BaseModel):
    """
    Represents an order.
    """
    id: int
    customer_id: int
    total_amount: float
    status: str


# Example Order response model (replace with your actual model)
class OrderResponse(BaseModel):
    """
    Represents the response model for an order.
    """
    id: int
    customer_id: int
    total_amount: float
    status: str


# Example dependency (replace with your actual database/service dependency)
async def get_orders_dependency():
    """
    Simulates fetching orders from a database or service.
    Replace with your actual implementation.
    """
    # In a real application, this would fetch data from a database or service.
    # For this example, we return a static list of orders.
    orders = [
        Order(id=1, customer_id=101, total_amount=100.0, status="Pending"),
        Order(id=2, customer_id=102, total_amount=200.0, status="Shipped"),
        Order(id=3, customer_id=101, total_amount=150.0, status="Delivered"),
    ]
    return orders


router = APIRouter()


@router.get(
    "/orders",
    response_model=List[OrderResponse],
    summary="List Orders",
    description="Retrieve a list of orders with optional filtering and pagination.",
    tags=["orders"],
)
async def list_orders(
    customer_id: Optional[int] = Query(
        None, description="Filter orders by customer ID"
    ),
    status: Optional[str] = Query(None, description="Filter orders by status"),
    skip: int = Query(0, description="Number of orders to skip"),
    limit: int = Query(10, description="Maximum number of orders to return"),
    orders: List[Order] = Depends(get_orders_dependency),
):
    """
    Retrieves a list of orders, optionally filtered by customer ID and status,
    with pagination support.

    Args:
        customer_id (Optional[int]): Filter orders by customer ID.
        status (Optional[str]): Filter orders by status.
        skip (int): Number of orders to skip for pagination.
        limit (int): Maximum number of orders to return.
        orders (List[Order]): Dependency providing the list of orders.

    Returns:
        List[OrderResponse]: A list of orders matching the filter criteria,
        limited by the pagination parameters.

    Raises:
        HTTPException: If no orders are found matching the criteria (status_code=404).
    """
    filtered_orders = orders

    if customer_id is not None:
        filtered_orders = [
            order for order in filtered_orders if order.customer_id == customer_id
        ]

    if status is not None:
        filtered_orders = [
            order for order in filtered_orders if order.status == status
        ]

    # Apply pagination
    paginated_orders = filtered_orders[skip : skip + limit]

    if not paginated_orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders found matching the criteria.",
        )

    return paginated_orders
```