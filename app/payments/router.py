from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.auth.dependencies import owner_required, driver_required
from app.database.database import get_db
from app.payments.schemas import PaymentHistoryResponse
from app.payments.service import get_payment_history
from app.models.payment import Payment
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payments"])

class SubmitCashRequest(BaseModel):
    submitted_to: str

@router.patch("/{payment_id}/submit-cash")
def submit_cash(
    payment_id: int, 
    req: SubmitCashRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(driver_required)
):
    payment = db.query(Payment).filter(
        Payment.id == payment_id, 
        Payment.submitted_by == current_user.id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found.")
    
    # FIX: Removed .value because payment_location is now a string
    if payment.payment_location != "CASH":
        raise HTTPException(status_code=400, detail="Only cash payments require a handoff name.")

    payment.cash_submitted_to = req.submitted_to
    db.commit()
    return {"message": "Cash submission recorded."}

@router.get("/history", response_model=list[PaymentHistoryResponse])
def payment_history(db: Session = Depends(get_db), current_user=Depends(owner_required)):
    return get_payment_history(db)