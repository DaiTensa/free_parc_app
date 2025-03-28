# main.py
from fastapi import FastAPI
from app.routes import users, parkingspots, auth, reservations

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(parkingspots.router, prefix="/parkingspots", tags=["Parking Spots"])
app.include_router(auth.router, prefix="/auth", tags=["User Login"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])


@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de gestion de places de parking !"}

# Lancer avec `uvicorn app.main:app --reload`

