```python
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

# Example database model (replace with your actual model)
class Order(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    status: str

# Example database dependency (replace with your actual database connection)
async def get_db():
    """
    Simulates a database connection.  Replace with your actual database connection logic.
    """
    try:
        # Simulate a database connection
        yield
    finally:
        # Simulate closing the database connection
        pass

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderListResponse(BaseModel):
    """
    Response model for listing orders.
    """
    orders: List[Order]
    total: int
    page: int
    page_size: int


@router.get(
    "/",
    response_model=OrderListResponse,
    summary="List orders",
    description="Retrieve a list of orders with pagination support.",
)
async def list_orders(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    db=Depends(get_db),  # noqa: B008
) -> OrderListResponse:
    """
    Endpoint to list orders with pagination.

    Args:
        page: The page number to retrieve.
        page_size: The number of orders per page.
        db: Database dependency.

    Returns:
        A list of orders with pagination information.

    Raises:
        HTTPException: If there is an error retrieving the orders.
    """
    try:
        # Simulate fetching orders from the database with pagination
        # Replace this with your actual database query
        all_orders = [
            Order(id=1, customer_id=101, total_amount=100.0, status="Shipped"),
            Order(id=2, customer_id=102, total_amount=200.0, status="Pending"),
            Order(id=3, customer_id=101, total_amount=150.0, status="Delivered"),
            Order(id=4, customer_id=103, total_amount=300.0, status="Shipped"),
            Order(id=5, customer_id=102, total_amount=250.0, status="Pending"),
        ]
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        orders = all_orders[start_index:end_index]
        total = len(all_orders)

        return OrderListResponse(
            orders=orders, total=total, page=page, page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve orders: {e}",
        )
```