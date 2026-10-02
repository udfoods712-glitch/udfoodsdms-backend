from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.core.enums import DeliveryStatus
from app.models.user import User


def get_owner_dashboard(db: Session):

    today_deliveries = (
        db.query(Delivery)
        .filter(
            func.date(Delivery.scheduled_date) == date.today()
        )
        .order_by(
            Delivery.scheduled_date.asc()
        )
        .all()
    )

    scheduled_today = sum(
        1
        for delivery in today_deliveries
        if delivery.status == DeliveryStatus.SCHEDULED
    )

    in_transit_today = sum(
        1
        for delivery in today_deliveries
        if delivery.status == DeliveryStatus.IN_TRANSIT
    )

    completed_today = sum(
        1
        for delivery in today_deliveries
        if delivery.status == DeliveryStatus.COMPLETED
    )

    return {
        "total_today": len(today_deliveries),
        "scheduled_today": scheduled_today,
        "in_transit_today": in_transit_today,
        "completed_today": completed_today,
        "deliveries": today_deliveries
    }


def get_driver_dashboard(
    driver: User,
    db: Session
):

    current_delivery = (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver.id,
            Delivery.status == DeliveryStatus.IN_TRANSIT
        )
        .first()
    )

    scheduled_deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver.id,
            Delivery.status == DeliveryStatus.SCHEDULED
        )
        .order_by(
            Delivery.scheduled_date.asc()
        )
        .all()
    )

    return {
        "current_delivery": current_delivery,
        "scheduled_deliveries": scheduled_deliveries
    }