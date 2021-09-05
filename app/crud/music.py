from sqlalchemy.orm import Session

import app.models.music as models
import app.schemas.music as schemas

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist._id == artist_id).first()

def get_artist_by_spotify_id(db: Session, artist_id: str):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()

def get_artist_by_name(db: Session, artist_name: str):
    return db.query(models.Artist).filter(models.Artist.name == artist_name).first()

def get_artists(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Artist).offset(skip).limit(limit).all()

def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return db_artist


def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album._id == album_id).first()

def get_album_by_spotify_id(db: Session, album_id: str):
    return db.query(models.Album).filter(models.Album.id == album_id).first()

def get_albums_by_artist(db: Session, artist_id: str):
    return db.query(models.Album).filter(artist_id in models.Album.artist_id).all()

def get_albums(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Album).offset(skip).limit(limit).all()

def create_album(db: Session, album: schemas.AlbumCreate, artist_ids: list):
    db_album = models.Album(**album.dict(), artist_id=artist_ids)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)

    return db_album


def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track._id == track_id).first()

def get_track_by_spotify_id(db: Session, track_id: str):
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def get_tracks_by_album(db: Session, album_id: int):
    return db.query(models.Track).filter(models.Track.album_id == album_id).all()

def get_tracks_by_artist(db: Session, artist_id: int):
    return db.query(models.Track).filter(artist_id in models.Track.artist_id).all()

def get_tracks(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Track).offset(skip).limit(limit).all()

def create_track(db: Session, track: schemas.TrackCreate, album_id: int, artist_ids: list):
    db_track = models.Album(**track.dict(), album_id=album_id, artist_id=artist_ids)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)

    return db_track
