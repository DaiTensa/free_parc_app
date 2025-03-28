from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import ParkingSpot, Reservation
from app.schemas import ReservationCreate, ReservationResponse
from app.crud import create_reservation, end_reservation

router = APIRouter()

@router.post("/", response_model=ReservationResponse)
def reserve_parking_spot(reservation_data: ReservationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Permet à un utilisateur connecté de réserver une place de parking."""
    parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == reservation_data.parking_spot_id).first()
    
    if not parking_spot:
        raise HTTPException(status_code=404, detail="Place de parking introuvable")

    reservation = create_reservation(db, reservation_data, current_user.id)
    
    return reservation

@router.put("/{reservation_id}/end", response_model=ReservationResponse)
def finish_reservation(reservation_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Permet à un utilisateur de terminer une réservation."""
    reservation = end_reservation(db, reservation_id, current_user.id)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation introuvable ou non autorisée")
    
    return reservation


@router.get("/available")
def get_current_reservations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Retourne la liste des réservation pour un utilisateur."""
    current_reservations = db.query(Reservation).filter(Reservation.end_time == "string", Reservation.user_id == current_user.id).all()
    return [{"id": current_reservation.id, "parking_spot_id": current_reservation.parking_spot_id, "start_time": current_reservation.start_time} for current_reservation in current_reservations]