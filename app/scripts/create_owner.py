from sqlalchemy.orm import Session

# Added engine and Base to create tables
from app.database.database import SessionLocal, engine
from app.database.base import Base
from app.models import User, Delivery, Payment 

from app.core.config import settings
from app.core.enums import UserRole
from app.auth.security import hash_password

def create_owner():
    # --- NEW: This line creates all your tables in Neon ---
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        existing_owner = (
            db.query(User)
            .filter(User.role == UserRole.OWNER)
            .first()
        )

        if existing_owner:
            print("Owner already exists.")
            return

        owner = User(
            name=settings.FIRST_OWNER_NAME,
            phone=settings.FIRST_OWNER_PHONE,
            email=settings.FIRST_OWNER_EMAIL,
            password_hash=hash_password(
                settings.FIRST_OWNER_PASSWORD
            ),
            role=UserRole.OWNER,
            is_active=True,
            must_change_password=False
        )

        db.add(owner)
        db.commit()
        db.refresh(owner)
        print("Owner created successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    create_owner()