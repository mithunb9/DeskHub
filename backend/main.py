from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import spotipy

from spotify import SpotifyController

load_dotenv()
controller = SpotifyController()

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
@app.get("/spotify")
def spotify_home():
    if controller.get_client():
        return {"status": "Online", "auth": "Authenticated"}
    return {"status": "Online", "auth": "Not Authenticated", "login_url": "/spotify/login"}


@app.get("/spotify/login")
def spotify_login():
    return RedirectResponse(controller.get_auth_url())


@app.get("/spotify/callback")
def spotify_callback(code: str):
    controller.handle_auth_code(code)
    return {"message": "Auth successful. You may close this window."}


@app.get("/spotify/now-playing")
def spotify_now_playing():
    try:
        data = controller.get_current_track()
        if not data:
            return {"status": "Nothing playing or not authenticated"}
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/spotify/control/{action}")
def spotify_playback_control(action: str, value: int = None):
    client = controller.get_client()
    if not client:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        if action == "play":
            controller.play()
        elif action == "pause":
            controller.pause()
        elif action == "next":
            controller.next_track()
        elif action == "prev":
            controller.previous_track()
        elif action == "volume":
            if value is None:
                raise HTTPException(status_code=400, detail="Volume value required")
            controller.set_volume(value)
        else:
            raise HTTPException(status_code=404, detail="Action not found")

        return {"status": "success", "action": action}

    except spotipy.exceptions.SpotifyException as e:
        if "NO_ACTIVE_DEVICE" in str(e):
            raise HTTPException(
                status_code=503,
                detail="No active Spotify device found. Open Spotify on a device first.",
            )
        raise HTTPException(status_code=500, detail=str(e))