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
                        "customer_id": "789a1234-b567-89c0-d123-456789abcdef",
                        "order_date": "2024-01-01",
                        "total_amount": 100.00
                    },
                    {
                        "order_id": "234f5678-f90c-23e4-b567-537725285111",
                        "customer_id": "890b2345-c678-90d1-e234-567890abcdef",
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
                "customer_id": "789a1234-b567-89c0-d123-456789abcdef",
                "order_date": "2024-01-01",
                "total_amount": 100.00
            },
            {
                "order_id": "234f5678-f90c-23e4-b567-537725285111",
                "customer_id": "890b2345-c678-90d1-e234-567890abcdef",
                "order_date": "2024-01-02",
                "total_amount": 200.00
            }
        ]
    )


class OrderListRequestParams(BaseModel):
    """
    Pydantic model for representing request parameters for listing orders.

    Attributes:
        limit (Optional[int]): The maximum number of orders to return. Defaults to 10.
            Example: 10
        offset (Optional[int]): The number of orders to skip. Defaults to 0.
            Example: 0
    """
    limit: Optional[int] = Field(
        10,
        description="The maximum number of orders to return. Defaults to 10.",
        example=10
    )
    offset: Optional[int] = Field(
        0,
        description="The number of orders to skip. Defaults to 0.",
        example=0
    )

    @validator("limit")
    def limit_must_be_positive(cls, value: int) -> int:
        """
        Validator to ensure that the limit is a positive integer.

        Args:
            value (int): The limit value.

        Returns:
            int: The limit value if it is valid.

        Raises:
            ValueError: If the limit is not a positive integer.
        """
        if value <= 0:
            raise ValueError("Limit must be a positive integer.")
        return value

    @validator("offset")
    def offset_must_be_non_negative(cls, value: int) -> int:
        """
        Validator to ensure that the offset is a non-negative integer.

        Args:
            value (int): The offset value.

        Returns:
            int: The offset value if it is valid.

        Raises:
            ValueError: If the offset is not a non-negative integer.
        """
        if value < 0:
            raise ValueError("Offset must be a non-negative integer.")
        return value
```