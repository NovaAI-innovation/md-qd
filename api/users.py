```python
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field

from core.security import get_password_hash, verify_password
from db.session import get_db
from models.user import User
from sqlalchemy.orm import Session

router = APIRouter()


class UserUpdate(BaseModel):
    """
    Represents the data required to update a user.
    """
    full_name: Optional[str] = Field(None, description="User's full name")
    email: Optional[str] = Field(None, description="User's email address")
    password: Optional[str] = Field(None, description="User's password")
    is_active: Optional[bool] = Field(None, description="User's active status")


@router.put("/{user_id}", response_model=None,
            summary="Update a user by ID",
            description="Updates an existing user with the provided information.")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
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
            - 400 if the email is already in use by another user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found"
        )

    # Update fields if provided
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.email is not None:
        # Check if the email is already in use by another user
        existing_user = db.query(User).filter(User.email == user_update.email, User.id != user_id).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )
        user.email = user_update.email
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    db.commit()
    db.refresh(user)

    return {"message": f"User with ID {user_id} updated successfully"}
```