from datetime import datetime
from pydantic import BaseModel

class DeliveryCreate(BaseModel):
    consignment_name: str
    amount: float
    delivery_address: str
    notes: str | None = None
    driver_id: int | None = None  # Now Optional
    scheduled_date: datetime

class AssignDriverRequest(BaseModel):
    driver_id: int

class DeliveryResponse(BaseModel):
    id: int
    consignment_name: str
    amount: float
    delivery_address: str
    notes: str | None
    driver_id: int | None
    driver_name: str
    created_by: int
    status: str
    scheduled_date: datetime
    
    # New payment details for the Archive check
    payment_id: int | None = None
    payment_location: str | None = None
    cash_submitted_to: str | None = None

    class Config:
        from_attributes = True