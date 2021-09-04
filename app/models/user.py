"""
Specify user-related models
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy_json import mutable_json_type

from app.database import Base
from app.models.music import Tracks

class User(Base):
    """
    _id 
    country 
    display_name 
    email
    explicit_content
    external_urls
    followers
    href
    id
    images
    product
    type
    uri
    """
    __tablename__ = "users"

    _id = Column(Integer, primary_key=True, index=True)
    country = Column(String, default='US', length=2)
    display_name = Column(String, length=50)
    email = Column(String, length=150, unique=True, index=True)
    explicit_content = Column(mutable_json_type(dbtype=JSONB, nested=True))
    external_urls = Column(mutable_json_type(dbtype=JSONB, nested=True))
    followers = Column(mutable_json_type(dbtype=JSONB, nested=True))
    href = Column(String, length=150)
    id = Column(String, length=50, unique=True, index=True)
    images = Column(mutable_json_type(dbtype=JSONB, nested=True))
    product = Column(String, length=50)
    type = Column(String, length=50)
    uri = Column(String, length=150)

    playlists = relationship("Playlist", back_populates="owner")


class Playlist(Base):
    """
    collaborative
    description
    external_urls
    followers
    href
    id
    images
    name
    owner
    primary_color
    public
    snapshot_id
    tracks
    type
    uri
    """
    __tablename__ = "playlists"

    _id = Column(Integer, primary_key=True, index=True)
    collaborative = Column(Boolean, default=False)
    description = Column(String, length=150)
    external_urls = Column(mutable_json_type(dbtype=JSONB, nested=True))
    followers = Column(mutable_json_type(dbtype=JSONB, nested=True))
    href = Column(String, length=150)
    id = Column(String, length=50, unique=True, index=True)
    images = Column(mutable_json_type(dbtype=JSONB, nested=True))
    name = Column(String, length=150)
    owner_id = Column(Integer, ForeignKey("users._id"), index=True)
    primary_color = Column(String, length=6, nullable=True)
    public = Column(Boolean, default=False)
    snapshot_id = Column(String, length=150)
    type = Column(String, length=50)
    uri = Column(String, length=150)

    tracks = relationship("Tracks", secondary="playlist_tracks")


class PlaylistTracksAssociation(Base):
    """
    Playlist & Tracks association table

    Note that playlists and tracks don't have cascade. When a playlist (or track) is deleted the 
        tracks (or playlist) must not be affected.
    """
    __tablename__ = "playlist_tracks"

    _id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists._id"))
    track_id = Column(Integer, ForeignKey("tracks._id"))

    playlist = relationship("Playlist", backref=backref("playlist_tracks"))
    track = relationship(Tracks, backref=backref("playlist_tracks"))

