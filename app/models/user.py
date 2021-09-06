"""
Specify user-related models
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base

class User(Base):
    """
    _id: local DB id
    id: spotify id
    """
    __tablename__ = "users"

    _id = Column(Integer, primary_key=True, index=True)
    country = Column(String(length=2), default='US')
    display_name = Column(String(length=50))
    email = Column(String(length=150), unique=True, index=True)
    href = Column(String(length=150))
    id = Column(String(length=50), unique=True, index=True)
    product = Column(String(length=50))
    type = Column(String(length=50))
    uri = Column(String(length=150))

    playlists = relationship("Playlist", back_populates="owner")


class Playlist(Base):
    """
    _id: local DB id
    id: spotify id
    """
    __tablename__ = "playlists"

    _id = Column(Integer, primary_key=True, index=True)
    collaborative = Column(Boolean, default=False)
    description = Column(String(length=150))
    href = Column(String(length=150))
    id = Column(String(length=50), unique=True, index=True)
    name = Column(String(length=150))
    owner_id = Column(Integer, ForeignKey("users._id"), index=True)
    public = Column(Boolean, default=False)
    snapshot_id = Column(String(length=150))
    type = Column(String(length=50))
    uri = Column(String(length=150))

    tracks = relationship("Track", secondary="playlist_tracks")
    owner = relationship("User", back_populates="playlists")


class PlaylistTracks(Base):
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
    track = relationship("Track", backref=backref("playlist_tracks"))
