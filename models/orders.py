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
        description="A list of order dictionaries.",
        example=[
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
    )


class OrderListRequestParams(BaseModel):
    """
    Pydantic model for representing request parameters for listing orders.

    Attributes:
        limit (Optional[int]): Maximum number of orders to return.
            Example: 10
        offset (Optional[int]): Offset for pagination.
            Example: 0
    """
    limit: Optional[int] = Field(
        None,
        description="Maximum number of orders to return.",
        example=10
    )
    offset: Optional[int] = Field(
        None,
        description="Offset for pagination.",
        example=0
    )

    @validator("limit")
    def limit_must_be_positive(cls, value: Optional[int]) -> Optional[int]:
        """
        Validator to ensure that the limit is a positive integer.
        """
        if value is not None and value <= 0:
            raise ValueError("Limit must be a positive integer.")
        return value

    @validator("offset")
    def offset_must_be_non_negative(cls, value: Optional[int]) -> Optional[int]:
        """
        Validator to ensure that the offset is a non-negative integer.
        """
        if value is not None and value < 0:
            raise ValueError("Offset must be a non-negative integer.")
        return value
```