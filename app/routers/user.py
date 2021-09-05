from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models.user as models
import app.schemas.user as schemas
import app.crud.user as crud


router = APIRouter(
    prefix='/v1',
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


# Users

@router.post('/users', response_model=schemas.User)
def create_user(user:schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if bool(db_user):
        raise HTTPException(status_code=400, detail="email already registered")
    return crud.create_user(db=db, user=user)

@router.get('/user/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@router.get('/user/find', response_model=schemas.User)
def find_user(db: Session=Depends(get_db), email: Optional[str]=None, spotify_id: Optional[str]=None):
    if email is not None:
        db_user = crud.get_user_by_email(db, email=email)
    elif spotify_id is not None:
        db_user = crud.get_user_by_spotify_id(db, user_id=spotify_id)
    else:
        return {}

    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

# @router.put('/user/{user_id}', response_model=schemas.User)
# def update_user(user_id: int, db: Session=Depends(get_db)):


# Playlists
