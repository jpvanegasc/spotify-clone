from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models.user as models
import app.schemas.user as schemas
import app.crud.user as crud


user_router = APIRouter(
    prefix='/v1',
    tags=["users"]
)

playlist_router = APIRouter(
    prefix='/v1',
    tags=["playlists"]
)

def get_db():
    db = SessionLocal()
    yield db


# Users

@user_router.post('/users', response_model=schemas.User)
def create_user(user:schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, user_email=user.email)
    if bool(db_user):
        raise HTTPException(status_code=400, detail="email already registered")
    return crud.create_user(db=db, user=user)

@user_router.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

@user_router.get('/users/find', response_model=schemas.User)
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

@user_router.get('/users', response_model=schemas.User)
def read_users(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit)
    if not bool(db_users):
        raise HTTPException(status_code=404, detail="users not found")
    return db_users

@user_router.put('/users/{user_id}', response_model=schemas.UserCreate)
def update_user(user_id: int, user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db_user.update(user.dict())
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.delete('/users/{user_id}', status_code=204)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db_user.delete()
    db.commit()
    return {}

# Playlists

@playlist_router.post('/playlists', response_model=schemas.Playlist)
def create_playlist(playlist:schemas.PlaylistCreate, user_id: int, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist_by_spotify_id(db, playlist_id=playlist.id)
    if bool(db_playlist):
        raise HTTPException(status_code=400, detail="playlist already exists")
    return crud.create_playlist(db=db, playlist=playlist)

@playlist_router.get('/playlists/{playlist_id}', response_model=schemas.Playlist)
def read_playlist(playlist_id: int, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    return db_playlist

@playlist_router.get('/users/{user_id}/playlists', response_model=schemas.Playlist)
def get_user_playlists(user_id:int, db: Session=Depends(get_db)):
    db_playlists = crud.get_playlists_by_user(db=db, user_id=user_id)
    if not bool(db_playlists):
        raise HTTPException(status_code=404, detail="playlists not found")
    return db_playlists

@playlist_router.put('/playlists/{playlist_id}', response_model=schemas.PlaylistCreate)
def update_playlist(playlist_id: int, playlist: schemas.PlaylistCreate, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id)
    if playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    db_playlist.update(playlist.dict())
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@playlist_router.delete('/playlists/{user_id}', status_code=204)
def delete_playlist(playlist_id: int, db: Session=Depends(get_db)):
    db_playlist = crud.get_playlist(db=db, playlist_id=playlist_id)
    if db_playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    db_playlist.delete()
    db.commit()
    return {}
