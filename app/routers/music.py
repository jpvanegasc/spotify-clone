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
    yield db

# Artists

@artist_router.post('/artists')
def create_artist(artist: schemas.ArtistCreate, db: Session=Depends(get_db)):
    artist = crud.get_artist_by_name(db=db, artist_name=artist.name)
    if bool(artist):
        raise HTTPException(status_code=400, detail="artist already exists")
    return crud.create_artist(db=db, artist=artist)

@artist_router.get('/artists/{artist_id}')
def read_artist(artist_id: int, db: Session=Depends(get_db)):
    artist = crud.get_artist(db=db, artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    return artist

@artist_router.get('/artists')
def read_artists(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    artists = crud.get_artists(db=db, skip=skip, limit=limit)
    if not bool(artists):
        raise HTTPException(status_code=404, detail="artists not found")
    return artists

@artist_router.put('/artists/{artist_id}')
def update_artist(artist_id: int, artist: schemas.ArtistCreate, db: Session=Depends(get_db)):
    db_artist = crud.get_artist(db=db, artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    db_artist.update(artist.dict())
    db.commit()
    db.refresh(db_artist)
    return db_artist

@artist_router.delete('/artists/{artist_id}', status_code=204)
def delete_artist(artist_id: int, db: Session=Depends(get_db)):
    artist = crud.get_artist(db=db, artist_id=artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="artist not found")
    artist.delete()
    artist.commit()
    return {}

# Albums

@album_router.post('/albums')
def create_album(album: schemas.AlbumCreate, db: Session=Depends(get_db)):
    album = crud.get_album_by_spotify_id(db=db, album_id=album.id)
    if bool(album):
        raise HTTPException(status_code=400, detail="album already exists")
    return crud.create_album(db=db, album=album)

@album_router.get('/albums/{album_id}')
def read_album(album_id: int, db: Session=Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="album not found")
    return album

@album_router.get('/albums')
def read_albums(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    albums = crud.get_albums(db=db, skip=skip, limit=limit)
    if not bool(albums):
        raise HTTPException(status_code=404, detail="albums not found")
    return albums

@album_router.put('/albums/{album_id}')
def update_album(album_id: int, album: schemas.AlbumCreate, db: Session=Depends(get_db)):
    db_album = crud.get_album(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="album not found")
    db_album.update(album.dict())
    db.commit()
    db.refresh(db_album)
    return db_album

@album_router.delete('/albums/{album_id}', status_code=204)
def delete_album(album_id: int, db: Session=Depends(get_db)):
    album = crud.get_album(db=db, album_id=album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="album not found")
    album.delete()
    album.commit()
    return {}

# Tracks

@track_router.post('/tracks')
def create_track(track: schemas.TrackCreate, db: Session=Depends(get_db)):
    track = crud.get_track_by_spotify_id(db=db, track_id=track.id)
    if bool(track):
        raise HTTPException(status_code=400, detail="track already exists")
    return crud.create_track(db=db, track=track)

@track_router.get('/tracks/{track_id}')
def read_track(track_id: int, db: Session=Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")
    return track

@track_router.get('/tracks')
def read_tracks(skip: Optional[int]=0, limit: Optional[int]=100, db: Session=Depends(get_db)):
    tracks = crud.get_tracks(db=db, skip=skip, limit=limit)
    if not bool(tracks):
        raise HTTPException(status_code=404, detail="tracks not found")
    return tracks

@track_router.put('/tracks/{track_id}')
def update_track(track_id: int, track: schemas.TrackCreate, db: Session=Depends(get_db)):
    db_track = crud.get_track(db=db, track_id=track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")
    db_track.update(track.dict())
    db.commit()
    db.refresh(db_track)
    return db_track

@track_router.delete('/tracks/{track_id}', status_code=204)
def delete_track(track_id: int, db: Session=Depends(get_db)):
    track = crud.get_track(db=db, track_id=track_id)
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")
    track.delete()
    track.commit()
    return {}

@track_router.patch('playlists/{playlist_id}/tracks/{track_id}')
def add_track_to_playlist(playlist_id: int, track_id: int, db: Session=Depends(get_db)):
    playlist = user_crud.get_playlist(db=db, playlist_id=playlist_id)
    track = crud.get_track(db=db, track_id=track_id)

    if playlist is None:
        raise HTTPException(status_code=404, detail="playlist not found")
    if track is None:
        raise HTTPException(status_code=404, detail="track not found")

    playlist.tracks.append(track)
    db.commit()
    db.refresh(playlist)

    return track
