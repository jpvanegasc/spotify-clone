from sqlalchemy.orm import Session
import traceback

import app.models.user as models
import app.schemas.user as schemas

# Users

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user(db: Session, user: schemas.UserCreate, db_user: models.User):
    for key in user.dict().keys():
        setattr(db_user, key, user.dict()[key])

    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()
    return

# Playlists

def get_playlist(db: Session, playlist_id: int):
    return db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()

def get_playlists(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Playlist).offset(skip).limit(limit).all()

def create_playlist(db: Session, playlist: schemas.PlaylistCreate):
    db_playlist = models.Playlist(**playlist.dict())
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    return db_playlist

def update_playlist(db: Session, playlist: schemas.PlaylistCreate, db_playlist: models.Playlist):
    for key in playlist.dict().keys():
        setattr(db_playlist, key, playlist.dict()[key])

    db.commit()
    db.refresh(db_playlist)

    return db_playlist

def delete_playlist(db: Session, db_playlist: models.Playlist):
    db.delete(db_playlist)
    db.commit()
    return
