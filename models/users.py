```python
from typing import Optional, List

from pydantic import BaseModel, Field, validator, EmailStr


class UserUpdate(BaseModel):
    """
    Pydantic model for updating user information.

    Attributes:
        first_name (Optional[str]): The first name of the user. Example: "John".
        last_name (Optional[str]): The last name of the user. Example: "Doe".
        email (Optional[EmailStr]): The email address of the user. Example: "john.doe@example.com".
        age (Optional[int]): The age of the user. Must be a non-negative integer. Example: 30.
        is_active (Optional[bool]): Whether the user is active. Example: True.
        roles (Optional[List[str]]): A list of roles assigned to the user. Example: ["admin", "editor"].
    """
    first_name: Optional[str] = Field(default=None, description="The first name of the user. Example: John")
    last_name: Optional[str] = Field(default=None, description="The last name of the user. Example: Doe")
    email: Optional[EmailStr] = Field(default=None, description="The email address of the user. Example: john.doe@example.com")
    age: Optional[int] = Field(default=None, description="The age of the user. Must be a non-negative integer. Example: 30")
    is_active: Optional[bool] = Field(default=None, description="Whether the user is active. Example: True")
    roles: Optional[List[str]] = Field(default=None, description="A list of roles assigned to the user. Example: ['admin', 'editor']")

    @validator("age")
    def validate_age(cls, age: Optional[int]) -> Optional[int]:
        """
        Validates that the age is a non-negative integer.

        Args:
            age (Optional[int]): The age to validate.

        Returns:
            Optional[int]: The validated age.

        Raises:
            ValueError: If the age is negative.
        """
        if age is not None and age < 0:
            raise ValueError("Age must be a non-negative integer.")
        return age
```