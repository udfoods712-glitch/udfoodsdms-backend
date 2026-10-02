from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    delivery_id = Column(
        Integer,
        ForeignKey("deliveries.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    # Changed from Enum to String to prevent crashes from old test data
    payment_location = Column(
        String(50),
        nullable=False
    )

    cash_submitted_to= Column(
        String(255),
        nullable=True
    )

    submitted_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    delivery = relationship(
        "Delivery",
        foreign_keys=[delivery_id]
    )

    driver = relationship(
        "User",
        foreign_keys=[submitted_by]
    )

    @property
    def consignment_name(self):
        return self.delivery.consignment_name

    @property
    def driver_name(self):
        return self.driver.name