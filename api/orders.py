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

# Example Order list response model
class OrderList(BaseModel):
    """
    Represents a list of orders.
    """
    orders: List[Order]
    total: int
    page: int
    page_size: int

# In-memory order storage (replace with a database)
orders_db = [
    Order(id=1, customer_id=101, total_amount=100.0, status="pending"),
    Order(id=2, customer_id=102, total_amount=200.0, status="shipped"),
    Order(id=3, customer_id=101, total_amount=150.0, status="delivered"),
]

router = APIRouter()

@router.get(
    "/orders",
    response_model=OrderList,
    summary="List orders",
    description="Retrieve a list of orders with pagination support.",
)
async def list_orders(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    status_filter: Optional[str] = Query(None, description="Filter by order status"),
) -> OrderList:
    """
    Retrieve a list of orders with pagination and optional status filtering.

    Args:
        page: The page number to retrieve (default: 1).
        page_size: The number of orders per page (default: 10).
        status_filter: Optional filter to retrieve orders with a specific status.

    Returns:
        A list of orders with pagination information.

    Raises:
        HTTPException: If there are any errors during the process.
    """
    try:
        # Apply status filter if provided
        filtered_orders = orders_db
        if status_filter:
            filtered_orders = [order for order in orders_db if order.status == status_filter]

        # Calculate pagination indices
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        # Paginate the results
        paginated_orders = filtered_orders[start_index:end_index]

        # Create the response
        order_list = OrderList(
            orders=paginated_orders,
            total=len(filtered_orders),
            page=page,
            page_size=page_size,
        )

        return order_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving orders: {str(e)}",
        )
```