```python
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field

from core.users import update_user, get_user
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()


class UserUpdate(BaseModel):
    """
    Represents the data required to update a user.
    """
    first_name: Optional[str] = Field(default=None, title="First Name", max_length=50)
    last_name: Optional[str] = Field(default=None, title="Last Name", max_length=50)
    email: Optional[str] = Field(default=None, title="Email", max_length=100)
    is_active: Optional[bool] = Field(default=None, title="Is Active")

    class Config:
        """
        Pydantic config
        """
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "is_active": True
            }
        }


@router.put("/{user_id}", response_model=None,
            summary="Update a user by ID",
            description="Updates an existing user with the provided information.",
            response_description="The updated user information.")
def update_user_endpoint(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Updates a user in the database.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The data to update the user with.
        db (Session): The database session.

    Returns:
        dict: A message indicating the update was successful.

    Raises:
        HTTPException:
            - 404 if the user is not found.
            - 500 for any other error during the update process.
    """
    try:
        # Check if the user exists
        existing_user = get_user(db, user_id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Update the user
        updated_user = update_user(db, user_id, user_update.dict(exclude_unset=True))

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )

        return {"message": f"User with id {user_id} updated successfully."}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
```