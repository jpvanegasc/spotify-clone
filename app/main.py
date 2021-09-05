import uvicorn

from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker

from .routers import user, music
from .database import engine
import app.models.user as user_models
import app.models.music as music_models

user_models.Base.metadata.create_all(bind=engine)
music_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.user_router)
app.include_router(user.playlist_router)
app.include_router(music.artist_router)
app.include_router(music.album_router)
app.include_router(music.track_router)

@app.get("/ping")
def health_check():
    return {"message":"API is up and running!"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
