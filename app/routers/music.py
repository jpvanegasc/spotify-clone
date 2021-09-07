from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models.music as models
import app.schemas.music as schemas
import app.crud.music as crud

artist_router = APIRouter(
    prefix='/v1',
    tags=["Artists"]
)

album_router = APIRouter(
    prefix='/v1',
    tags=["Albums"]
)

track_router = APIRouter(
    prefix='/v1',
    tags=["Tracks"]
)

def get_db():
    yield SessionLocal()

# Artists

@artist_router.post('/artists')
def create_artist(artist:schemas.ArtistCreate, db: Session=Depends(get_db)):
    db_artist = crud.get_artist_by_name(db=db, artist_name=artist.name)
    if bool(db_artist):
        raise HTTPException(status_code=400, detail="artist already registered")
    return crud.create_artist(db=db, artist=artist)

@artist_router.get('/artists/{artist_id}')
def read_artist(artist_id: int, db: Session=Depends(get_db)):
    db_artist = crud.get_artist(db=db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    return db_artist

@artist_router.get('/artists')
def read_artists(skip: Optional[int]=0, limit: Optional[int]=10, db: Session=Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="limit exceeds permited value")

    db_artists = crud.get_artists(db, skip=skip, limit=limit)
    if not bool(db_artists):
        raise HTTPException(status_code=404, detail="artists not found")
    return db_artists

@artist_router.put('/artists/{artist_id}')
def update_artist(artist_id: int, artist: schemas.ArtistCreate, db: Session=Depends(get_db)):
    db_artist = crud.get_artist(db=db, artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    return crud.update_artist(db=db, artist=artist, db_artist=db_artist)

@artist_router.delete('/artists/{artist_id}')
def delete_artist(artist_id: int, db: Session=Depends(get_db)):
    db_artist = crud.get_artist(db=db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    crud.delete_artist(db=db, db_artist=db_artist)
    return Response(status_code=204)

# Albums

@album_router.post('/albums')
def create_album(album:schemas.AlbumCreate, db: Session=Depends(get_db)):
    db_artists = []

    for artist_id in album.artists_id:
        artist = crud.get_artist(db=db, artist_id=artist_id)
        if artist is None:
            raise HTTPException(status_code=400, detail="artist not found")
        else:
            db_artists.append(artist)

    db_album = crud.create_album(db=db, album=album)
    db_album.artist.extend(db_artists)
    db.commit()
    db.refresh(db_album)

    return db_album

@album_router.get('/albums/{album_id}')
def read_album(album_id: int, db: Session=Depends(get_db)):
    db_album = crud.get_album(db=db, album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="album not found")
    return db_album

@album_router.put('/albums/{album_id}')
def update_album(album_id: int, album: schemas.AlbumCreate, db: Session=Depends(get_db)):
    db_album = crud.get_album(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="album not found")
    return crud.update_album(db=db, album=album, db_album=db_album)

@album_router.delete('/albums/{album_id}')
def delete_album(album_id: int, db: Session=Depends(get_db)):
    db_album = crud.get_album(db=db, album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="album not found")
    crud.delete_album(db=db, db_album=db_album)
    return Response(status_code=204)

# Tracks

@track_router.post('/tracks')
def create_track(track:schemas.TrackCreate, db: Session=Depends(get_db)):
    db_album = crud.get_album(db=db, album_id=track.album_id)
    if db_album is None:
        raise HTTPException(status_code=400, detail="album not found")

    db_artists = []

    for artist_id in track.artists_id:
        artist = crud.get_artist(db=db, artist_id=artist_id)
        if artist is None:
            raise HTTPException(status_code=400, detail="artist not found")
        else:
            db_artists.append(artist)

    db_track = crud.create_track(db=db, track=track)
    db_track.artist.extend(db_artists)
    db.commit()
    db.refresh(db_track)

    return db_track

@track_router.get('/tracks/{track_id}')
def read_track(track_id: int, db: Session=Depends(get_db)):
    db_track = crud.get_track(db=db, track_id=track_id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="track not found")
    return db_track

@track_router.put('/tracks/{track_id}')
def update_track(track_id: int, track: schemas.TrackCreate, db: Session=Depends(get_db)):
    db_track = crud.get_track(db=db, track_id=track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")
    return crud.update_track(db=db, track=track, db_track=db_track)

@track_router.delete('/tracks/{track_id}')
def delete_track(track_id: int, db: Session=Depends(get_db)):
    db_track = crud.get_track(db=db, track_id=track_id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="track not found")
    crud.delete_track(db=db, db_track=db_track)
    return Response(status_code=204)
