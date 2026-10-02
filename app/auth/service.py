from sqlalchemy.orm import Session

from app.models.user import User

from fastapi import HTTPException

from app.auth.security import (
    verify_password,
    create_access_token,
    hash_password
)


def authenticate_user(
    phone: str,
    password: str,
    db: Session
):

    user = (
        db.query(User)
        .filter(User.phone == phone)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    if not user.is_active:
        return None

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role.value
        }
    )

    return {
        "user": user,
        "token": token
    }


def change_password(
    current_user: User,
    password_data,
    db: Session
):

    if not verify_password(
        password_data.current_password,
        current_user.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect."
        )

    current_user.password_hash = hash_password(
        password_data.new_password
    )

    current_user.must_change_password = False

    db.commit()

    db.refresh(current_user)

    return {
        "message": "Password changed successfully."
    }


def reset_password(
    phone: str,
    db: Session
):

    user = (
        db.query(User)
        .filter(User.phone == phone)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found with this phone number."
        )

    default_password = "Driver@123"

    user.password_hash = hash_password(
        default_password
    )

    user.must_change_password = True

    db.commit()

    db.refresh(user)

    return {
        "message": "Password reset successfully."
    }