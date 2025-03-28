# routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.crud import create_user, get_users
from app.database import get_db

router = APIRouter()

@router.post("/new", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    
    new_user = create_user(db, user)

    if isinstance(new_user, dict) and "error" in new_user:
        raise HTTPException(status_code=400, detail=new_user["error"])
    else:
        # Si l'utilisateur a été créé avec succès, retourner l'utilisateur
        return create_user(db, user)


@router.get("/all", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)
