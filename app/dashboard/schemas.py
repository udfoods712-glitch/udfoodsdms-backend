from datetime import datetime

from pydantic import BaseModel

from app.core.enums import DeliveryStatus


class ActiveDeliveryResponse(BaseModel):
    id: int
    consignment_name: str
    delivery_address: str
    amount: float
    driver_id: int | None = None
    status: DeliveryStatus
    scheduled_date: datetime

    class Config:
        from_attributes = True


class OwnerDashboardResponse(BaseModel):
    total_today: int
    scheduled_today: int
    in_transit_today: int
    completed_today: int
    deliveries: list[ActiveDeliveryResponse]


class DriverDashboardResponse(BaseModel):
    current_delivery: ActiveDeliveryResponse | None
    scheduled_deliveries: list[ActiveDeliveryResponse]