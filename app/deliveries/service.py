from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.payment import Payment

from app.core.enums import DeliveryStatus, UserRole
from app.models.delivery import Delivery
from app.models.user import User
from datetime import date
from sqlalchemy import func


def create_delivery(delivery, owner: User, db: Session):
    # Only verify driver if an ID is provided
    if delivery.driver_id is not None:
        driver = (
            db.query(User)
            .filter(User.id == delivery.driver_id, User.role == UserRole.DRIVER, User.is_active == True)
            .first()
        )
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found.")

    new_delivery = Delivery(
        consignment_name=delivery.consignment_name,
        amount=delivery.amount,
        delivery_address=delivery.delivery_address,
        notes=delivery.notes,
        driver_id=delivery.driver_id,
        created_by=owner.id,
        scheduled_date=delivery.scheduled_date,
        status=DeliveryStatus.SCHEDULED
    )

    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)

    return new_delivery

def get_today_deliveries(db: Session):

    deliveries = (
        db.query(Delivery)
        .filter(
            func.date(Delivery.scheduled_date) == date.today()
        )
        .order_by(Delivery.scheduled_date.asc())
        .all()
    )

    return deliveries

def get_my_deliveries(
    driver: User,
    db: Session
):

    deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver.id
        )
        .order_by(
            Delivery.scheduled_date.asc()
        )
        .all()
    )

    return deliveries

def start_delivery(
    delivery_id: int,
    driver: User,
    db: Session
):

    active_delivery = (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver.id,
            Delivery.status == DeliveryStatus.IN_TRANSIT
        )
        .first()
    )

    if active_delivery:
        raise HTTPException(
            status_code=400,
            detail="Finish current delivery first."
        )

    delivery = (
        db.query(Delivery)
        .filter(
            Delivery.id == delivery_id,
            Delivery.driver_id == driver.id
        )
        .first()
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found."
        )

    if delivery.status == DeliveryStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Delivery is already completed."
        )

    delivery.status = DeliveryStatus.IN_TRANSIT

    delivery.started_at = datetime.utcnow()

    db.commit()

    db.refresh(delivery)

    return delivery

from datetime import datetime


def complete_delivery(
    delivery_id: int,
    payment_data,
    driver: User,
    db: Session
):
    delivery = (
        db.query(Delivery)
        .filter(
            Delivery.id == delivery_id,
            Delivery.driver_id == driver.id
        )
        .first()
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found."
        )

    if delivery.status != DeliveryStatus.IN_TRANSIT:
        raise HTTPException(
            status_code=400,
            detail="Delivery is not in transit."
        )

    delivery.status = DeliveryStatus.COMPLETED
    delivery.completed_at = datetime.utcnow()

    payment = Payment(
        delivery_id=delivery.id,
        amount=delivery.amount,
        # ADD .value HERE to convert Enum to the raw String
        payment_location=payment_data.payment_location.value, 
        submitted_by=driver.id
    )

    db.add(payment)
    db.commit()
    db.refresh(delivery)

    return delivery

def get_driver_archive(
    driver: User,
    db: Session
):

    return (
        db.query(Delivery)
        .filter(
            Delivery.driver_id == driver.id,
            Delivery.status == DeliveryStatus.COMPLETED
        )
        .order_by(
            Delivery.completed_at.desc()
        )
        .all()
    )

def get_delivery_archive(db: Session):

    return (
        db.query(Delivery)
        .order_by(
            Delivery.created_at.desc()
        )
        .all()
    )

# Add this function to the bottom of app/deliveries/service.py

def assign_driver_to_delivery(delivery_id: int, driver_id: int, db: Session):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found.")
        
    driver = db.query(User).filter(User.id == driver_id, User.role == UserRole.DRIVER).first()
    
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found.")
        
    delivery.driver_id = driver.id
    db.commit()
    db.refresh(delivery)
    
    return delivery