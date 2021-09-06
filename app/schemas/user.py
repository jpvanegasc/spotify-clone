"""
Define User-related schemas
"""
from typing import List, Optional

from pydantic import BaseModel, Json, constr

from app.schemas.music import Track

class PlaylistBase(BaseModel):
    collaborative: bool
    description: constr(max_length=150)
    href: constr(max_length=150)
    id: constr(max_length=50)
    name: constr(max_length=150)
    owner_id: int
    public: bool
    snapshot_id: constr(max_length=150)
    type: constr(max_length=50)
    uri: constr(max_length=150)

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    _id: int
    tracks: List[Track] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    country: constr(max_length=2)
    display_name: constr(max_length=50)
    email: constr(max_length=150)
    href: constr(max_length=150)
    id: constr(max_length=50)
    product: constr(max_length=50)
    type: constr(max_length=50)
    uri: constr(max_length=150)

class UserCreate(UserBase):
    pass

class User(UserBase):
    _id: int
    playlists: List[Playlist]

    class Config:
        orm_mode = True
