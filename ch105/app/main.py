from fastapi import FastAPI
from decouple import config

app = FastAPI()

@app.get("/")
def read_env():
    return {
        "api_secret": config("API_SECRET_KEY"),
        "debug_mode": config("DEBUG", cast=bool)
    }
