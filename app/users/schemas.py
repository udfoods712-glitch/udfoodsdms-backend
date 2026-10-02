from pydantic import BaseModel, EmailStr
from app.core.enums import UserRole


class DriverCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    vehicle_number: str


class DriverResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    vehicle_number: str
    is_active: bool

    class Config:
        from_attributes = True

class DriverUpdate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    vehicle_number: str

class OwnerCreate(BaseModel):
    name: str
    phone: str
    email: str


class OwnerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str | None = None
    vehicle_number: str | None = None
    role: UserRole
    is_active: bool
    must_change_password: bool

    class Config:
        from_attributes = True