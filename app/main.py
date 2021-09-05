import uvicorn

from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker

# from .config import DATABASE_URL

from .routers import user
from .database import engine
import app.models.user as user_models
import app.models.music as music_models

user_models.Base.metadata.create_all(bind=engine)
music_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.user_router)
app.include_router(user.playlist_router)

@app.get("/")
def hello_world():
    return "hello world"


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
