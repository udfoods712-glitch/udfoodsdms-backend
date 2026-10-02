from datetime import datetime
from pydantic import BaseModel
from app.core.enums import PaymentLocation

class CompleteDeliveryRequest(BaseModel):
    payment_location: PaymentLocation

class PaymentHistoryResponse(BaseModel):
    id: int
    consignment_name: str
    driver_name: str
    amount: float
    payment_location: str  
    submitted_at: datetime
    cash_submitted_to: str | None = None # <-- ADDED THIS LINE

    class Config:
        from_attributes = True