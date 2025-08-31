```python
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class OrderListResponse(BaseModel):
    """
    Pydantic model for representing a list of orders.

    Attributes:
        orders (List[dict]): A list of order dictionaries.
            Example:
                [
                    {
                        "order_id": "123e4567-e89b-12d3-a456-426614174000",
                        "customer_id": "456e4567-e89b-12d3-a456-426614174001",
                        "order_date": "2024-01-01",
                        "total_amount": 100.00
                    },
                    {
                        "order_id": "789e4567-e89b-12d3-a456-426614174002",
                        "customer_id": "101e4567-e89b-12d3-a456-426614174003",
                        "order_date": "2024-01-02",
                        "total_amount": 200.00
                    }
                ]
    """
    orders: List[dict] = Field(
        ...,
        description="A list of order dictionaries."
    )


class OrderFilter(BaseModel):
    """
    Pydantic model for filtering orders.

    Attributes:
        customer_id (Optional[str]): Filter orders by customer ID.
            Example: "456e4567-e89b-12d3-a456-426614174001"
        order_date (Optional[str]): Filter orders by order date (YYYY-MM-DD).
            Example: "2024-01-01"
        min_total_amount (Optional[float]): Filter orders with total amount greater than or equal to this value.
            Example: 50.00
        max_total_amount (Optional[float]): Filter orders with total amount less than or equal to this value.
            Example: 150.00
    """
    customer_id: Optional[str] = Field(
        None,
        description="Filter orders by customer ID. Example: '456e4567-e89b-12d3-a456-426614174001'"
    )
    order_date: Optional[str] = Field(
        None,
        description="Filter orders by order date (YYYY-MM-DD). Example: '2024-01-01'"
    )
    min_total_amount: Optional[float] = Field(
        None,
        description="Filter orders with total amount greater than or equal to this value. Example: 50.00"
    )
    max_total_amount: Optional[float] = Field(
        None,
        description="Filter orders with total amount less than or equal to this value. Example: 150.00"
    )

    @validator("order_date")
    def validate_order_date(cls, value: Optional[str]) -> Optional[str]:
        """
        Validates the order date format (YYYY-MM-DD).

        Args:
            value (Optional[str]): The order date string.

        Returns:
            Optional[str]: The validated order date string.

        Raises:
            ValueError: If the order date format is invalid.
        """
        if value:
            try:
                from datetime import datetime
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid order date format.  Use YYYY-MM-DD.")
        return value
```