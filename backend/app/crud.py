# crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, ParkingSpot, Reservation
from app.schemas import UserCreate, ParkingSpotCreate, ReservationCreate
from app.auth import get_password_hash
from datetime import datetime, timezone

def create_user(db: Session, user: UserCreate):
    """Créer un npouveau utilisateur dans la base de données."""
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)).first()
    
    if existing_user:
        # Si l'utilisateur existe déjà, retourner une erreur
        return {"error": f"Le nom {user.username} avec cet email {user.email} existe déjà."}
    

    # Créer un nouvel utilisateur
    # Utiliser la fonction get_password_hash pour hacher le mot de passe
    password = get_password_hash(user.password)
    
    # Si l'utilisateur n'existe pas, créer un nouvel utilisateur
    try:
        # Ajouter l'utilisateur à la session
        db_user = User(username=user.username, email=user.email, password_hash=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    # Gérer les erreurs d'intégrité (par exemple, si l'email ou le nom d'utilisateur est déjà pris)
    except IntegrityError:
        db.rollback()
        print("Erreur d'intégrité lors de la création de l'utilisateur.")
        return None


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_parking_spot(db: Session, spot: ParkingSpotCreate):
    db_spot = ParkingSpot(name=spot.name, location=spot.location, is_available=True)
    db.add(db_spot)
    db.commit()
    db.refresh(db_spot)
    return db_spot



def create_reservation(db: Session, reservation_data: ReservationCreate, user_id: int):
    """Crée une réservation avec la date de début automatique."""
    reservation = Reservation(
        user_id=user_id,
        parking_spot_id=reservation_data.parking_spot_id,
        start_time=datetime.now(timezone.utc),  # Date et heure actuelles
        end_time=reservation_data.end_time  # Laisser l'utilisateur spécifier l'heure de fin
    )

    db.add(reservation)
    # Mettre à jour la place de parking comme non disponible
    parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == reservation_data.parking_spot_id).first()
    if parking_spot:
        parking_spot.is_available = False  # Place occupée
        
    db.commit()
    db.refresh(reservation)
    return reservation


def end_reservation(db: Session, reservation_id: int, user_id: int):
    """Met fin à une réservation et rend la place de parking disponible."""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id, Reservation.user_id == user_id).first()

    if not reservation or reservation.end_time != "string":  # Vérifiez si la réservation existe et si elle n'est pas déjà terminée
        return None  # Retourne None si la réservation n'existe pas ou ne correspond pas à l'utilisateur
    
    # Mettre à jour l'heure de fin avec l'heure actuelle
    reservation.end_time = datetime.now(timezone.utc)
    
    # Rendre la place de parking disponible
    parking_spot = db.query(ParkingSpot).filter(ParkingSpot.id == reservation.parking_spot_id).first()
    if parking_spot:
        parking_spot.is_available = True  # Assurez-vous que cette colonne existe dans votre modèle ParkingSpot
    
    db.commit()
    db.refresh(reservation)
    
    return reservation
