```python
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field

from api.dependencies import get_user_service
from services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])


class UserUpdate(BaseModel):
    """
    Represents the data required to update a user.
    """
    first_name: Optional[str] = Field(default=None, title="First Name", max_length=50)
    last_name: Optional[str] = Field(default=None, title="Last Name", max_length=50)
    email: Optional[str] = Field(default=None, title="Email Address")
    is_active: Optional[bool] = Field(default=None, title="Active Status")

    @classmethod
    def validate(cls, values: dict):
        """
        Validates the user update data.  Ensures at least one field is being updated.
        """
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update.")
        return values


@router.patch("/{user_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    """
    Updates an existing user.

    Args:
        user_id (int): The ID of the user to update.
        user_data (UserUpdate): The data to update the user with.
        user_service (UserService): The user service dependency.

    Returns:
        dict: A message indicating the successful update.

    Raises:
        HTTPException:
            - 404 if the user is not found.
            - 400 if the provided data is invalid.
            - 500 for any unexpected server errors.
    """
    try:
        updated = await user_service.update_user(user_id, user_data.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return {"message": f"User with id {user_id} updated successfully"}
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}",
        )
```