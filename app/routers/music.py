from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models.music as models
import app.schemas.music as schemas
import app.crud.music as crud
import app.crud.user as user_crud

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
    db_artist = crud.get_artist_by_name(db=db, artist_email=artist.email)
    if bool(db_artist):
        raise HTTPException(status_code=400, detail="email already registered")
    return crud.create_artist(db=db, artist=artist)

@artist_router.get('/artists/{artist_id}')
def read_artist(artist_id: int, db: Session=Depends(get_db)):
    db_artist = crud.get_artist(db=db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    return db_artist

@artist_router.get('/artists')
def read_artists(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
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
def create_album(album:schemas.AlbumCreate, user_id: int, db: Session=Depends(get_db)):
    return crud.create_album(db=db, album=album)

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
def create_track(track:schemas.TrackCreate, user_id: int, db: Session=Depends(get_db)):
    return crud.create_track(db=db, track=track)

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

@track_router.patch('playlists/{playlist_id}/tracks/{track_id}')
def add_track_to_playlist(playlist_id: int, track_id: int, db: Session=Depends(get_db)):
    playlist = user_crud.crud.get_playlist(db=db, playlist_id=playlist_id)
    track = crud.get_track(db=db, track_id=track_id)

    if playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")

    playlist.tracks.append(track)
    db.commit()
    db.refresh(playlist)

    return track
