from sqlalchemy import Column, ForeignKey, Integer, Enum, String, DateTime, Boolean, Float, UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from .database import MyDB, db_connect


class User(MyDB):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Pour stocker le hash du mot de passe
    is_active = Column(Boolean, default=True)  # Si l'utilisateur est actif ou non

    reservations = relationship("Reservation", back_populates="user")
    parking_spots = relationship("ParkingSpot", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class ParkingSpot(MyDB):
    __tablename__ = 'parking_spots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)  # Nom de la place (par exemple 'P1', 'P2', etc.)
    location = Column(String)  # Adresse ou localisation de la place de parking
    latitude = Column(Float, nullable=False)  # Latitude GPS
    longitude = Column(Float, nullable=False)  # Longitude GPS
    is_available = Column(Boolean, default=True)  # Si la place est disponible
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="parking_spots")  # Relation avec la table User
    reservations = relationship("Reservation", back_populates="parking_spot")

    def __repr__(self):
        return f"<ParkingSpot(id={self.id}, name={self.name}, location={self.location}, available={self.is_available})>"


class Reservation(MyDB):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parking_spot_id = Column(Integer, ForeignKey('parking_spots.id'), nullable=False)
    start_time = Column(String)  # Heure de début de la réservation
    end_time = Column(String)    # Heure de fin de la réservation

    user = relationship("User", back_populates="reservations")
    parking_spot = relationship("ParkingSpot", back_populates="reservations")

    # Ajouter une contrainte pour s'assurer que la réservation ne chevauche pas une autre réservation
    __table_args__ = (
        UniqueConstraint('user_id', 'parking_spot_id', 'start_time', name='uq_user_parking_start'),
        UniqueConstraint('user_id', 'parking_spot_id', 'end_time', name='uq_user_parking_end')
    )

    def __repr__(self):
        return f"<Reservation(id={self.id}, user_id={self.user_id}, parking_spot_id={self.parking_spot_id}, start_time={self.start_time}, end_time={self.end_time})>"


class Image(MyDB):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parking_spot_id = Column(Integer, ForeignKey('parking_spots.id'), nullable=False)
    image_url = Column(String, nullable=False)  # L'URL ou le chemin de l'image

    parking_spot = relationship("ParkingSpot", backref="images")

    def __repr__(self):
        return f"<Image(id={self.id}, parking_spot_id={self.parking_spot_id}, image_url={self.image_url})>"


if __name__ == "__main__":
    # TESTING THE DATABASE CONNECTION
    db = db_connect()
    session = db()
    print("Database connection successful !")
    session.close()