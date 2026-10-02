from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.core.enums import DeliveryStatus


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)

    consignment_name = Column(String(255), nullable=False)

    amount = Column(Float, nullable=False)

    delivery_address = Column(String(500), nullable=False)

    notes = Column(Text)

    # Made driver_id nullable
    driver_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        Enum(DeliveryStatus),
        default=DeliveryStatus.SCHEDULED,
        nullable=False
    )

    scheduled_date = Column(DateTime(timezone=True), nullable=False)

    started_at = Column(DateTime(timezone=True))

    completed_at = Column(DateTime(timezone=True))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    driver = relationship(
        "User",
        foreign_keys=[driver_id],
        back_populates="deliveries"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by]
    )

    payments = relationship("Payment", back_populates="delivery")

    @property
    def driver_name(self):
        return self.driver.name if self.driver else "Unassigned"

    @property
    def payment_id(self):
        return self.payments[0].id if self.payments else None

    @property
    def payment_location(self):
        # FIX: Removed .value because payment_location is now a native string
        return self.payments[0].payment_location if self.payments else None

    @property
    def cash_submitted_to(self):
        # FIX: Added this property so the frontend can read the submission status
        return self.payments[0].cash_submitted_to if self.payments else None