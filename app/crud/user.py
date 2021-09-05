from sqlalchemy import Session

import app.models.user as models
import app.schemas.user as schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User._id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_user_by_spotify_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_playlist(db: Session, playlist_id: int):
    return db.query(models.Playlist).filter(models.Playlist._id == playlist_id).first()

def get_playlist_by_spotify_id(db: Session, playlist_id: str):
    return db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()

def get_playlists_by_user(db: Session, user_id: int, limit: int=0):
    return db.query(models.Playlist).filter(models.Playlist.owner_id == user_id).all()

def get_playlists(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Playlist).offset(skip).limit(limit).all()

def create_playlist(db: Session, playlist: schemas.PlaylistCreate, user_id: int):
    db_playlist = models.User(**playlist.dict(), owner_id=user_id)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    return db_playlist
