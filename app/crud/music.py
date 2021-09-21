from sqlalchemy.orm import Session

import app.models.music as models
import app.schemas.music as schemas

# Artists

def get_artist(db: Session, artist_id: int):
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

def update_artist(db: Session, artist: schemas.ArtistCreate, db_artist: models.Artist):
    for key in artist.dict().keys():
        setattr(db_artist, key, artist.dict()[key])

    db.commit()
    db.refresh(db_artist)

    return db_artist

def delete_artist(db: Session, db_artist: models.Artist):
    db.delete(db_artist)
    db.commit()
    return

# Albums

def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()

def get_albums(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Album).offset(skip).limit(limit).all()

def create_album(db: Session, album: schemas.AlbumCreate):
    album_dict = album.dict()
    album_dict.pop('artists_id')

    db_album = models.Album(**album_dict)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)

    return db_album

def update_album(db: Session, album: schemas.AlbumCreate, db_album: models.Album):
    for key in album.dict().keys():
        setattr(db_album, key, album.dict()[key])

    db.commit()
    db.refresh(db_album)

    return db_album

def delete_album(db: Session, db_album: models.Album):
    artist_albums = db.query(models.ArtistAlbums).filter(models.ArtistAlbums.album_id == db_album.id).first()
    db.delete(artist_albums)
    tracks = db.query(models.Track).filter(models.Track.album_id == db_album.id).all()
    for track in tracks:
        artist_track = db.query(models.ArtistTracks).filter(models.ArtistTracks.track_id == track.id).first()
        db.delete(artist_track)
        db.delete(track)
    db.delete(db_album)
    db.commit()
    return

# Tracks

def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def get_tracks(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Track).offset(skip).limit(limit).all()

def create_track(db: Session, track: schemas.TrackCreate):
    track_dict = track.dict()
    track_dict.pop('artists_id')

    db_track = models.Track(**track_dict)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)

    return db_track

def update_track(db: Session, track: schemas.TrackCreate, db_track: models.Track):
    for key in track.dict().keys():
        setattr(db_track, key, track.dict()[key])

    db.commit()
    db.refresh(db_track)

    return db_track

def delete_track(db: Session, db_track: models.Track):
    db.delete(db_track)
    db.commit()
    return
