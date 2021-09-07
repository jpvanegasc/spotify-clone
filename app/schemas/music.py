"""
Define Music-related schemas
"""
from typing import ForwardRef, List
from datetime import datetime

from pydantic import BaseModel, Json, constr, conlist

artist_forward_ref = ForwardRef("List[Artist]")
album_forward_ref = ForwardRef("List[Album]")
track_forward_ref = ForwardRef("List[Track]")

class ArtistBase(BaseModel):
    href: constr(max_length=150)
    name: constr(max_length=150)
    popularity: int
    type: constr(max_length=50)
    uri: constr(max_length=150)

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    albums: album_forward_ref = []
    tracks: track_forward_ref = []

    class Config:
        orm_mode = True

class AlbumBase(BaseModel):
    album_type: constr(max_length=150)
    href: constr(max_length=150)
    label: constr(max_length=150)
    name: constr(max_length=150)
    popularity: int
    total_tracks: int
    type: constr(max_length=50)
    uri: constr(max_length=150)

class AlbumCreate(AlbumBase):
    artists_id: conlist(int, min_items=1)

class Album(AlbumBase):
    id: int
    tracks: track_forward_ref = []

    class Config:
        orm_mode = True

class TrackBase(BaseModel):
    disc_number: int
    duration_ms: int
    explicit: bool
    href: constr(max_length=150)
    is_local: bool
    is_playable: bool
    name: constr(max_length=150)
    popularity: int
    preview_url: constr(max_length=150)
    track_number: int
    type: constr(max_length=50)
    uri: constr(max_length=150)

class TrackCreate(TrackBase):
    album_id: conlist(int, min_items=1)
    artist_id: conlist(int, min_items=1)

class Track(TrackBase):
    id: int
    album: album_forward_ref = []
    artist: artist_forward_ref = []

    class Config:
        orm_mode = True

Artist.update_forward_refs()
Album.update_forward_refs()
Track.update_forward_refs()
