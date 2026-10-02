from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.auth.dependencies import get_current_user

from app.database.database import get_db
from app.auth.dependencies import owner_required, get_current_user
from app.users.schemas import (
    DriverCreate,
    DriverResponse,
    DriverUpdate,
    OwnerCreate,
    OwnerResponse,
    UserProfileResponse
)
from app.models.user import User
from app.users.service import (
    create_driver,
    get_all_drivers,
    get_driver_by_id,
    update_driver,
    disable_driver,
    create_owner
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/drivers",
    response_model=DriverResponse
)
def add_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db),
    current_user=Depends(owner_required)
):

    return create_driver(
        driver,
        db
    )

@router.get(
    "/drivers",
    response_model=List[DriverResponse]
)
def list_drivers(
    db: Session = Depends(get_db),
    current_user=Depends(owner_required)
):

    return get_all_drivers(db)

@router.get(
    "/drivers/{driver_id}",
    response_model=DriverResponse
)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(owner_required)
):

    return get_driver_by_id(
        driver_id,
        db
    )

@router.put(
    "/drivers/{driver_id}",
    response_model=DriverResponse
)
def edit_driver(
    driver_id: int,
    driver: DriverUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(owner_required)
):

    return update_driver(
        driver_id,
        driver,
        db
    )

@router.patch(
    "/drivers/{driver_id}/disable",
    response_model=DriverResponse
)
def deactivate_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(owner_required)
):

    return disable_driver(
        driver_id,
        db
    )

@router.post(
    "/owners",
    response_model=OwnerResponse
)
def add_owner(
    owner: OwnerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):

    return create_owner(
        owner,
        db
    )

@router.get(
    "/me",
    response_model=UserProfileResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user