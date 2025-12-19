from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/apps")
async def get_apps():
    return [
        {"name": "Spotify"},
        {"name": "Timer"},
        {"name": "Calculator"},
        {"name": "Calendar"},
        {"name": "Messages"},
        {"name": "Weather"},
        {"name": "Settings"}
    ]

@app.get("/settings")
async def get_settings():
    return {
        "deviceName": "DeskHub",
        "timeFormat": "12h",   # or "24h"
        "theme": "dark",
        "wallpaper": "gradient"  # later: url
    }

""" SPOTIFY """