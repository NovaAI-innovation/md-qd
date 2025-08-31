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

    first_name: Optional[str] = Field(default=None, description="The first name of the user. Example: 'John'")
    last_name: Optional[str] = Field(default=None, description="The last name of the user. Example: 'Doe'")
    email: Optional[EmailStr] = Field(default=None, description="The email address of the user. Example: 'john.doe@example.com'")
    is_active: Optional[bool] = Field(default=None, description="Whether the user is active. Example: True")

    @validator("first_name")
    def first_name_must_be_alpha(cls, first_name: Optional[str]) -> Optional[str]:
        """
        Validator to ensure the first name contains only alphabetic characters.

        Args:
            first_name (Optional[str]): The first name to validate.

        Returns:
            Optional[str]: The validated first name.

        Raises:
            ValueError: If the first name contains non-alphabetic characters.
        """
        if first_name is not None and not first_name.isalpha():
            raise ValueError("First name must contain only alphabetic characters")
        return first_name

    @validator("last_name")
    def last_name_must_be_alpha(cls, last_name: Optional[str]) -> Optional[str]:
        """
        Validator to ensure the last name contains only alphabetic characters.

        Args:
            last_name (Optional[str]): The last name to validate.

        Returns:
            Optional[str]: The validated last name.

        Raises:
            ValueError: If the last name contains non-alphabetic characters.
        """
        if last_name is not None and not last_name.isalpha():
            raise ValueError("Last name must contain only alphabetic characters")
        return last_name
```