from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.payments.schemas import CompleteDeliveryRequest

from app.auth.dependencies import (
    owner_required,
    driver_required
)

from app.database.database import get_db
from app.deliveries.schemas import (
    DeliveryCreate,
    DeliveryResponse
)

from app.deliveries.service import (
    create_delivery,
    get_today_deliveries,
    get_my_deliveries,
    start_delivery,
    complete_delivery,
    get_driver_archive,
    get_delivery_archive
)

from app.models.delivery import Delivery
from app.models.user import User

from app.deliveries.schemas import AssignDriverRequest
from app.deliveries.service import assign_driver_to_delivery

router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"]
)


@router.post(
    "",
    response_model=DeliveryResponse
)
def add_delivery(
    delivery: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):

    return create_delivery(
        delivery,
        current_user,
        db
    )


@router.get(
    "/today",
    response_model=List[DeliveryResponse]
)
def today_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):

    return get_today_deliveries(db)


# ==========================================
# ADDRESS SUGGESTIONS
# ==========================================

@router.get(
    "/addresses",
    response_model=list[str]
)
def address_suggestions(
    query: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):

    query = query.strip()

    if not query:
        return []

    rows = (
        db.query(Delivery.delivery_address)
        .filter(
            Delivery.delivery_address.ilike(
                f"%{query}%"
            )
        )
        .order_by(
            Delivery.delivery_address.asc()
        )
        .limit(50)
        .all()
    )

    suggestions = []
    seen = set()

    for row in rows:
        address = row[0]

        if not address:
            continue

        normalized = address.strip().lower()

        if normalized in seen:
            continue

        seen.add(normalized)
        suggestions.append(address.strip())

        if len(suggestions) >= 10:
            break

    return suggestions


@router.get(
    "/my",
    response_model=list[DeliveryResponse]
)
def my_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(driver_required)
):

    return get_my_deliveries(
        current_user,
        db
    )

@router.patch(
    "/{delivery_id}/assign-driver",
    response_model=DeliveryResponse
)
def assign_driver_endpoint(
    delivery_id: int,
    req: AssignDriverRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):
    return assign_driver_to_delivery(
        delivery_id,
        req.driver_id,
        db
    )


@router.patch(
    "/{delivery_id}/start",
    response_model=DeliveryResponse
)
def start(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(driver_required)
):

    return start_delivery(
        delivery_id,
        current_user,
        db
    )


@router.patch(
    "/{delivery_id}/complete",
    response_model=DeliveryResponse
)
def complete(
    delivery_id: int,
    payment: CompleteDeliveryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(driver_required)
):

    return complete_delivery(
        delivery_id,
        payment,
        current_user,
        db
    )


@router.get(
    "/my/archive",
    response_model=list[DeliveryResponse]
)
def my_archive(
    db: Session = Depends(get_db),
    current_user: User = Depends(driver_required)
):

    return get_driver_archive(
        current_user,
        db
    )


@router.get(
    "/archive",
    response_model=list[DeliveryResponse]
)
def archive(
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_required)
):

    return get_delivery_archive(db)