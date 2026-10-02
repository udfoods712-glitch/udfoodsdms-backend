from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.deliveries.router import router as deliveries_router
from app.payments.router import router as payments_router
from app.dashboard.router import router as dashboard_router

app = FastAPI(
    title="Delivery Management API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(deliveries_router)
app.include_router(payments_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "Delivery Management API Running"
    }