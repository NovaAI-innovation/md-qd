```python
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field

from core.database import get_db
from core.models import User  # Assuming you have a User model
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


class UserUpdate(BaseModel):
    """
    Represents the data required to update a user.
    """

    username: str | None = Field(default=None, max_length=50, example="new_username")
    email: str | None = Field(default=None, example="new_email@example.com")
    full_name: str | None = Field(default=None, max_length=100, example="New Full Name")
    disabled: bool | None = Field(default=None, example=False)


@router.patch(
    "/{user_id}",
    response_model=User,
    summary="Update a user",
    description="Updates an existing user with the provided information.",
    response_description="The updated user.",
)
async def update_user(
    user_id: Annotated[int, Path(title="The ID of the user to update")],
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Updates an existing user in the database.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): The data to update the user with.
        db (Session): The database session.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException:
            - 404: If the user with the given ID is not found.
            - 400: If the update fails due to data validation errors or other issues.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Update the user object with the provided data
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update user: {str(e)}",
        )
```