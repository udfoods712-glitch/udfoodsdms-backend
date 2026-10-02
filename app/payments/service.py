from sqlalchemy.orm import Session

from app.models.payment import Payment


def get_payment_history(db: Session):

    return (
        db.query(Payment)
        .order_by(Payment.submitted_at.desc())
        .all()
    )