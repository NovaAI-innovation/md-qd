```python
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserUpdate(BaseModel):
    """
    Pydantic model for updating user information.

    Attributes:
        first_name (Optional[str]): The first name of the user. Example: "John".
        last_name (Optional[str]): The last name of the user. Example: "Doe".
        email (Optional[EmailStr]): The email address of the user. Example: "john.doe@example.com".
        is_active (Optional[bool]): Whether the user is active. Example: True.
    """

    first_name: Optional[str] = Field(default=None, description="The first name of the user. Example: John")
    last_name: Optional[str] = Field(default=None, description="The last name of the user. Example: Doe")
    email: Optional[EmailStr] = Field(default=None, description="The email address of the user. Example: john.doe@example.com")
    is_active: Optional[bool] = Field(default=None, description="Whether the user is active. Example: True")

    @validator("first_name", "last_name")
    def name_must_be_alpha(cls, value: Optional[str]) -> Optional[str]:
        """
        Validator to ensure that first_name and last_name contain only alphabetic characters.
        """
        if value is not None and not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value
```