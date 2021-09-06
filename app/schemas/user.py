"""
Define User-related schemas
"""
from typing import List, Optional

from pydantic import BaseModel, Json, constr

from app.schemas.music import Track

class PlaylistBase(BaseModel):
    collaborative: bool
    description: constr(max_length=150)
    external_urls: Json
    followers: Json
    href: constr(max_length=150)
    id: constr(max_length=50)
    images: Json
    name: constr(max_length=150)
    primary_color: Optional[constr(max_length=6)]=None
    public: bool
    snapshot_id: constr(max_length=150)
    type: constr(max_length=50)
    uri: constr(max_length=150)

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    _id: int
    owner_id: int
    tracks: List[Track] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    country: constr(max_length=2)
    display_name: constr(max_length=50)
    email: constr(max_length=150)
    explicit_content: Json
    external_urls: Json
    followers: Json
    href: constr(max_length=150)
    id: constr(max_length=50)
    images: Json
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
