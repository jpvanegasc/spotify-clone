"""
Specify music-related models
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean,DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base

class Artist(Base):
    """
    _id: local DB id
    id: spotify id
    """
    __tablename__ = "artists"

    _id = Column(Integer, primary_key=True, index=True)
    external_urls = Column(JSONB)
    followers = Column(JSONB)
    genres = Column(JSONB)
    href = Column(String(length=150))
    id = Column(String(length=50), unique=True, index=True)
    images = Column(JSONB)
    name = Column(String(length=150), unique=True, index=True)
    popularity = Column(Integer)
    type = Column(String(length=50))
    uri = Column(String(length=150))

    albums = relationship("Album", secondary="artist_albums")
    tracks = relationship("Album", secondary="artist_tracks")


class Album(Base):
    """
    _id: local DB id
    id: spotify id
    """
    __tablename__ = "albums"

    _id = Column(Integer, primary_key=True, index=True)
    album_type = Column(String(length=50))
    copyrights = Column(JSONB)
    external_ids = Column(JSONB)
    external_urls = Column(JSONB)
    genres = Column(JSONB)
    href = Column(String(length=150))
    id = Column(String(length=50), unique=True, index=True)
    images = Column(JSONB)
    label = Column(String(length=150))
    name = Column(String(length=150))
    popularity = Column(Integer)
    release_date = Column(DateTime)
    release_date_precision = Column(String(length=50))
    total_tracks = Column(Integer)
    type = Column(String(length=50))
    uri = Column(String(length=150))

    artist = relationship("Artist", secondary="artist_albums")
    tracks = relationship("Track", back_populates="album")


class Track(Base):
    """
    _id: local DB id
    id: spotify id
    """
    __tablename__ = "tracks"

    _id = Column(Integer, primary_key=True, index=True)
    album_id = Column(Integer, ForeignKey("albums._id"))
    disc_number = Column(Integer)
    duration_ms = Column(Integer)
    explicit = Column(Boolean, default=False)
    external_ids = Column(JSONB)
    external_urls = Column(JSONB)
    href = Column(String(length=150))
    id = Column(String(length=50), unique=True, index=True)
    is_local = Column(Boolean, default=False)
    is_playable = Column(Boolean, default=True)
    name = Column(String(length=150))
    popularity = Column(Integer)
    preview_url = Column(String(length=150))
    track_number = Column(Integer)
    type = Column(String(length=50))
    uri = Column(String(length=150))

    album = relationship("Album", back_populates="album")
    artist = relationship("Artist", secondary="artist_tracks")
    playlists = relationship("Playlist", secondary="playlist_tracks")


class ArtistAlbums(Base):
    """
    Artist & Albums association table
    """
    __tablename__ = "artist_albums"

    _id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists._id"))
    album_id = Column(Integer, ForeignKey("albums._id"))

    artist = relationship("Artist", backref=backref("artist_albums", cascade="delete-orphan"))
    album = relationship("Album", backref=backref("artist_albums"))


class ArtistTracks(Base):
    """
    Artist & Tracks association table
    """
    __tablename__ = "artist_tracks"

    _id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists._id"))
    track_id = Column(Integer, ForeignKey("tracks._id"))

    artist = relationship("Artist", backref=backref("artist_tracks", cascade="delete-orphan"))
    track = relationship("Track", backref=backref("artist_tracks"))
