from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.dependencies import (
    get_current_user,
    owner_required
)

from app.models.user import User

from app.auth.schemas import (
    LoginRequest,
    TokenResponse,
    ChangePasswordRequest,
    ResetPasswordRequest
)

from app.auth.service import (
    authenticate_user,
    change_password,
    reset_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):

    result = authenticate_user(
        credentials.phone,
        credentials.password,
        db
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone or password"
        )

    return TokenResponse(
        access_token=result["token"],
        token_type="bearer",
        must_change_password=
            result["user"].must_change_password
    )


@router.patch("/change-password")
def update_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return change_password(
        current_user,
        password_data,
        db
    )


@router.patch("/reset-password")
def reset_user_password(
    password_data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):

    return reset_password(
        password_data.phone,
        db
    )