# routes/parkingspots.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ParkingSpot
from app.schemas import ParkingSpotCreate, ParkingSpotResponse
from typing import List
from app.auth import get_current_user  # Import de l'authentification

router = APIRouter()

@router.post("/create", response_model=ParkingSpotResponse)
def create_parking_spot(
    spot: ParkingSpotCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Vérifie l'authentification
):
    """
    Créer une nouvelle place de parking.
    L'utilisateur doit être authentifié.
    """
    # Vérifier si une place avec le même nom existe déjà
    existing_spot = db.query(ParkingSpot).filter(ParkingSpot.name == spot.name).first()
    if existing_spot:
        raise HTTPException(status_code=400, detail="Une place avec ce nom existe déjà.")

    # Création de la place avec l'ID de l'utilisateur authentifié
    new_spot = ParkingSpot(
        name=spot.name,
        location=spot.location,
        latitude=spot.latitude,
        longitude=spot.longitude,
        owner_id=current_user.id,  # Utilisation de l'ID de l'utilisateur connecté
        is_available=True
    )

    db.add(new_spot)
    db.commit()
    db.refresh(new_spot)

    return new_spot

@router.get("/available")
def get_available_parking_spots(db: Session = Depends(get_db)):
    """Retourne la liste des places de parking disponibles."""
    available_spots = db.query(ParkingSpot).filter(ParkingSpot.is_available == True).all()
    return [{"id": spot.id, "location": spot.location, "longitude": spot.longitude, "latitude":spot.latitude} for spot in available_spots]