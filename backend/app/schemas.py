# schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class ParkingSpotCreate(BaseModel):
    name: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    # owner_id: int  # ID de l'utilisateur qui crée la place


class ParkingSpotResponse(BaseModel):
    id: int
    name: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_available: bool
    owner_id: int  # Pour savoir à qui appartient la place

    class Config:
        orm_mode = True

class ReservationCreate(BaseModel):
    user_id: int
    parking_spot_id: int
    end_time: str

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    parking_spot_id: int
    start_time: str
    end_time: str | None

    class Config:
        orm_mode = True
