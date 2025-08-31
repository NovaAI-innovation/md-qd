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
                        "order_id": "ORD-123",
                        "customer_id": "CUST-456",
                        "order_date": "2023-10-26",
                        "total_amount": 100.00
                    },
                    {
                        "order_id": "ORD-456",
                        "customer_id": "CUST-789",
                        "order_date": "2023-10-27",
                        "total_amount": 200.00
                    }
                ]
    """

    orders: List[dict] = Field(
        ...,
        description="A list of order dictionaries.",
        example=[
            {
                "order_id": "ORD-123",
                "customer_id": "CUST-456",
                "order_date": "2023-10-26",
                "total_amount": 100.00,
            },
            {
                "order_id": "ORD-456",
                "customer_id": "CUST-789",
                "order_date": "2023-10-27",
                "total_amount": 200.00,
            },
        ],
    )


class OrderListRequestParams(BaseModel):
    """
    Pydantic model for representing request parameters for listing orders.

    Attributes:
        limit (Optional[int]): The maximum number of orders to return. Defaults to 10.
            Example: 10
        offset (Optional[int]): The offset to start returning orders from. Defaults to 0.
            Example: 0
    """

    limit: Optional[int] = Field(
        10, description="The maximum number of orders to return.", example=10
    )
    offset: Optional[int] = Field(
        0, description="The offset to start returning orders from.", example=0
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