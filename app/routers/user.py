from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models.user as models
import app.schemas.user as schemas
import app.crud.user as crud


user_router = APIRouter(
    prefix='/v1',
    tags=["Users"]
)

playlist_router = APIRouter(
    prefix='/v1',
    tags=["Playlists"]
)

def get_db():
    yield SessionLocal()


# Users

@user_router.post('/users')
def create_user(user:schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user.email)
    if bool(db_user):
        raise HTTPException(status_code=400, detail="email already registered")
    return crud.create_user(db=db, user=user)

@user_router.get('/users/{user_id}')
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@user_router.get('/users')
def read_users(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit)
    if not bool(db_users):
        raise HTTPException(status_code=404, detail="users not found")
    return db_users

@user_router.put('/users/{user_id}')
def update_user(user_id: int, user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return crud.update_user(db=db, user=user, db_user=db_user)

@user_router.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    crud.delete_user(db=db, db_user=db_user)
    return Response(status_code=204)

# Playlists

@playlist_router.post('/playlists')
def create_playlist(playlist:schemas.PlaylistCreate, user_id: int, db: Session=Depends(get_db)):
    return crud.create_playlist(db=db, playlist=playlist)

@playlist_router.get('/playlists/{playlist_id}')
def read_playlist(playlist_id: int, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    return db_playlist

@playlist_router.put('/playlists/{playlist_id}')
def update_playlist(playlist_id: int, playlist: schemas.PlaylistCreate, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    return crud.update_playlist(db=db, playlist=playlist, db_playlist=db_playlist)

@playlist_router.delete('/playlists/{playlist_id}')
def delete_playlist(playlist_id: int, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    crud.delete_playlist(db=db, db_playlist=db_playlist)
    return Response(status_code=204)
