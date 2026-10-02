from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import (
    owner_required,
    driver_required
)

from app.dashboard.schemas import (
    OwnerDashboardResponse,
    DriverDashboardResponse
)

from app.dashboard.service import (
    get_owner_dashboard,
    get_driver_dashboard
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/owner",
    response_model=OwnerDashboardResponse
)
def owner_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(owner_required)
):

    return get_owner_dashboard(db)


@router.get(
    "/driver",
    response_model=DriverDashboardResponse
)
def driver_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(driver_required)
):

    return get_driver_dashboard(
        current_user,
        db
    )