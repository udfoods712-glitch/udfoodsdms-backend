from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.core.enums import UserRole
from app.auth.security import hash_password


def create_driver(driver, db: Session):

    existing = (
        db.query(User)
        .filter(User.phone == driver.phone)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists."
        )

    new_driver = User(
        name=driver.name,
        phone=driver.phone,
        email=driver.email,
        vehicle_number=driver.vehicle_number,
        password_hash=hash_password("Driver@123"),
        role=UserRole.DRIVER,
        is_active=True,
        must_change_password=True
    )

    db.add(new_driver)

    db.commit()

    db.refresh(new_driver)

    return new_driver

def get_all_drivers(db: Session):

    drivers = (
        db.query(User)
        .filter(User.role == UserRole.DRIVER)
        .all()
    )

    return drivers

def get_driver_by_id(
    driver_id: int,
    db: Session
):

    driver = (
        db.query(User)
        .filter(
            User.id == driver_id,
            User.role == UserRole.DRIVER
        )
        .first()
    )

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found."
        )

    return driver

def update_driver(
    driver_id: int,
    driver_data,
    db: Session
):

    driver = (
        db.query(User)
        .filter(
            User.id == driver_id,
            User.role == UserRole.DRIVER
        )
        .first()
    )

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found."
        )

    driver.name = driver_data.name
    driver.phone = driver_data.phone
    driver.email = driver_data.email
    driver.vehicle_number = driver_data.vehicle_number

    db.commit()

    db.refresh(driver)

    return driver

def disable_driver(
    driver_id: int,
    db: Session
):

    driver = (
        db.query(User)
        .filter(
            User.id == driver_id,
            User.role == UserRole.DRIVER
        )
        .first()
    )

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found."
        )

    driver.is_active = False

    db.commit()

    db.refresh(driver)

    return driver

def create_owner(owner, db: Session):

    existing = (
        db.query(User)
        .filter(User.phone == owner.phone)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists."
        )

    new_owner = User(
        name=owner.name,
        phone=owner.phone,
        email=owner.email,
        password_hash=hash_password("Owner@123"),
        role=UserRole.OWNER,
        is_active=True,
        must_change_password=True
    )

    db.add(new_owner)

    db.commit()

    db.refresh(new_owner)

    return new_owner