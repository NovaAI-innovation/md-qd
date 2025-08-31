```python
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class OrderListResponse(BaseModel):
    """
    Pydantic model for representing a list of orders in the API response.

    Attributes:
        orders (List[dict]): A list of order dictionaries.  Example: `[{"order_id": "123", "customer_id": "456", "total": 100.0}, {"order_id": "456", "customer_id": "789", "total": 200.0}]`
        total_count (int): The total number of orders available (for pagination purposes). Example: `100`
    """

    orders: List[dict] = Field(
        ...,
        description="A list of order dictionaries.  Example: `[{\"order_id\": \"123\", \"customer_id\": \"456\", \"total\": 100.0}, {\"order_id\": \"456\", \"customer_id\": \"789\", \"total\": 200.0}]`",
    )
    total_count: int = Field(
        ..., description="The total number of orders available (for pagination purposes). Example: `100`"
    )

    @validator("total_count")
    def total_count_must_be_positive(cls, value: int) -> int:
        """
        Validator to ensure that the total count is a non-negative integer.

        Args:
            value (int): The total count value.

        Returns:
            int: The validated total count value.

        Raises:
            ValueError: If the total count is negative.
        """
        if value < 0:
            raise ValueError("Total count must be a non-negative integer.")
        return value


class OrderListRequestParams(BaseModel):
    """
    Pydantic model for representing the request parameters for listing orders.

    Attributes:
        limit (Optional[int]): The maximum number of orders to return. Example: `10`
        offset (Optional[int]): The offset to start the list from (for pagination). Example: `0`
        customer_id (Optional[str]): Filter orders by customer ID. Example: `"cust123"`
    """

    limit: Optional[int] = Field(
        None, description="The maximum number of orders to return. Example: `10`"
    )
    offset: Optional[int] = Field(
        None, description="The offset to start the list from (for pagination). Example: `0`"
    )
    customer_id: Optional[str] = Field(
        None, description="Filter orders by customer ID. Example: `\"cust123\"`"
    )

    @validator("limit")
    def limit_must_be_positive(cls, value: Optional[int]) -> Optional[int]:
        """
        Validator to ensure that the limit is a positive integer if provided.

        Args:
            value (Optional[int]): The limit value.

        Returns:
            Optional[int]: The validated limit value.

        Raises:
            ValueError: If the limit is negative.
        """
        if value is not None and value <= 0:
            raise ValueError("Limit must be a positive integer.")
        return value

    @validator("offset")
    def offset_must_be_non_negative(cls, value: Optional[int]) -> Optional[int]:
        """
        Validator to ensure that the offset is a non-negative integer if provided.

        Args:
            value (Optional[int]): The offset value.

        Returns:
            Optional[int]: The validated offset value.

        Raises:
            ValueError: If the offset is negative.
        """
        if value is not None and value < 0:
            raise ValueError("Offset must be a non-negative integer.")
        return value
```