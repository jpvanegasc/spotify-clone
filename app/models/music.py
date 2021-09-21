"""
Specify music-related models
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base

class Artist(Base):
    """
    """
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    href = Column(String(length=150))
    name = Column(String(length=150), unique=True, index=True)
    popularity = Column(Integer)
    type = Column(String(length=50))
    uri = Column(String(length=150))

    albums = relationship("Album", secondary="artist_albums")
    tracks = relationship("Track", secondary="artist_tracks")


class Album(Base):
    """
    """
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    album_type = Column(String(length=50))
    href = Column(String(length=150))
    label = Column(String(length=150))
    name = Column(String(length=150))
    popularity = Column(Integer)
    total_tracks = Column(Integer)
    type = Column(String(length=50))
    uri = Column(String(length=150))

    artist = relationship("Artist", secondary="artist_albums")
    tracks = relationship("Track", back_populates="album")


class Track(Base):
    """
    """
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    album_id = Column(Integer, ForeignKey("albums.id"))
    disc_number = Column(Integer)
    duration_ms = Column(Integer)
    explicit = Column(Boolean, default=False)
    href = Column(String(length=150))
    is_local = Column(Boolean, default=False)
    is_playable = Column(Boolean, default=True)
    name = Column(String(length=150))
    popularity = Column(Integer)
    preview_url = Column(String(length=150))
    track_number = Column(Integer)
    type = Column(String(length=50))
    uri = Column(String(length=150))

    album = relationship("Album", back_populates="tracks")
    artist = relationship("Artist", secondary="artist_tracks")
    playlists = relationship("Playlist", secondary="playlist_tracks")


class ArtistAlbums(Base):
    """
    Artist & Albums association table
    """
    __tablename__ = "artist_albums"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))

    artist = relationship("Artist", backref=backref("artist_albums", cascade="delete-orphan"))
    album = relationship("Album", backref=backref("artist_albums", cascade="delete-orphan"))


class ArtistTracks(Base):
    """
    Artist & Tracks association table
    """
    __tablename__ = "artist_tracks"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))

    artist = relationship("Artist", backref=backref("artist_tracks", cascade="delete-orphan"))
    track = relationship("Track", backref=backref("artist_tracks"))
