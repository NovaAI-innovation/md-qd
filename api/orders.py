```python
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

# Example database models (replace with your actual models)
class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: str
    total_amount: float

# Example database interaction (replace with your actual database logic)
orders_db = [
    Order(order_id=1, customer_id=101, order_date="2023-01-01", total_amount=100.0),
    Order(order_id=2, customer_id=102, order_date="2023-01-05", total_amount=200.0),
    Order(order_id=3, customer_id=101, order_date="2023-01-10", total_amount=150.0),
]


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


class OrderResponse(BaseModel):
    """
    Response model for a single order.
    """

    order_id: int
    customer_id: int
    order_date: str
    total_amount: float


@router.get(
    "/",
    response_model=List[OrderResponse],
    summary="List orders",
    description="Retrieve a list of orders with optional pagination and filtering.",
)
async def list_orders(
    skip: int = Query(
        0,
        title="Skip",
        description="Number of orders to skip for pagination.",
        ge=0,
    ),
    limit: int = Query(
        10,
        title="Limit",
        description="Maximum number of orders to retrieve.",
        le=100,
    ),
    customer_id: Optional[int] = Query(
        None, title="Customer ID", description="Filter orders by customer ID."
    ),
) -> List[OrderResponse]:
    """
    Retrieve a list of orders with optional pagination and filtering.

    Args:
        skip: Number of orders to skip for pagination.
        limit: Maximum number of orders to retrieve.
        customer_id: Filter orders by customer ID.

    Returns:
        A list of OrderResponse objects.

    Raises:
        HTTPException: If there is an error retrieving the orders.
    """
    try:
        filtered_orders = orders_db
        if customer_id is not None:
            filtered_orders = [
                order for order in orders_db if order.customer_id == customer_id
            ]

        return filtered_orders[skip : skip + limit]  # Apply pagination
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve orders: {str(e)}",
        )
```