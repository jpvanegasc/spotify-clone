from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models.music as models
import app.schemas.music as schemas
import app.crud.music as crud

artist_router = APIRouter(
    prefix='/v1',
    tags=["artists"]
)

album_router = APIRouter(
    prefix='/v1',
    tags=["albums"]
)

track_router = APIRouter(
    prefix='/v1',
    tags=["tracks"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

# Artists

@artist_router.post('/artists', response_model=schemas.Artist)
def create_artist(artist: schemas.ArtistCreate, db: Session=Depends(get_db)):
    artist = crud.get_artist_by_name(db=db, artist_name=artist.name)
    if bool(artist):
        raise HTTPException(status_code=400, detail="artist already exists")
    return crud.create_artist(db=db, artist=artist)

@artist_router.get('/artists/{artist_id}', response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session=Depends(get_db)):
    artist = crud.get_artist(db=db, artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    return artist

@artist_router.get('/artists', response_model=schemas.Artist)
def read_artists(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    artists = crud.get_artists(db=db, skip=skip, limit=limit)
    if not bool(artists):
        raise HTTPException(status_code=404, detail="artists not found")
    return artists

# @artist_router.put('/artists/{artist_id}', response_model=schemas.Artist)

@artist_router.delete('/artists/{artist_id}', status_code=204)
def delete_artist(artist_id: int, db: Session=Depends(get_db)):
    artist = crud.get_artist(db=db, artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    artist.delete()
    artist.commit()
    return {}

# Albums

@album_router.post('/albums', response_model=schemas.Album)
def create_album(album: schemas.AlbumCreate, db: Session=Depends(get_db)):
    album = crud.get_album_by_spotify_id(db=db, album_id=album.id)
    if bool(album):
        raise HTTPException(status_code=400, detail="album already exists")
    return crud.create_album(db=db, album=album)

@album_router.get('/albums/{album_id}', response_model=schemas.Album)
def read_album(album_id: int, db: Session=Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="album not found")
    return album

@album_router.get('/albums', response_model=schemas.Album)
def read_albums(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    albums = crud.get_albums(db=db, skip=skip, limit=limit)
    if not bool(albums):
        raise HTTPException(status_code=404, detail="albums not found")
    return albums

# @album_router.put('/albums/{album_id}', response_model=schemas.Album)

@album_router.delete('/albums/{album_id}', status_code=204)
def delete_album(album_id: int, db: Session=Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="album not found")
    album.delete()
    album.commit()
    return {}

# Tracks

@track_router.post('/tracks', response_model=schemas.Track)
def create_track(track: schemas.TrackCreate, db: Session=Depends(get_db)):
    track = crud.get_track_by_spotify_id(db=db, track_id=track.id)
    if bool(track):
        raise HTTPException(status_code=400, detail="track already exists")
    return crud.create_track(db=db, track=track)

@track_router.get('/tracks/{track_id}', response_model=schemas.Track)
def read_track(track_id: int, db: Session=Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")
    return track

@track_router.get('/tracks', response_model=schemas.Track)
def read_tracks(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    tracks = crud.get_tracks(db=db, skip=skip, limit=limit)
    if not bool(tracks):
        raise HTTPException(status_code=404, detail="tracks not found")
    return tracks

# @track_router.put('/tracks/{track_id}', response_model=schemas.Track)

@track_router.delete('/tracks/{track_id}', status_code=204)
def delete_track(track_id: int, db: Session=Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")
    track.delete()
    track.commit()
    return {}

# TO-DO:
# endpoint for adding tracks to playlist
