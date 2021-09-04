from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import PROJECT_NAME, VERSION, DATABASE_URL

app = FastAPI(title=PROJECT_NAME, version=VERSION)

@app.get("/")
def hello_world():
    return "hello world"
