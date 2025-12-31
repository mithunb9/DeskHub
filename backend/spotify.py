import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import HTTPException

class SpotifyController:
    def __init__(self):
        # Load credentials from env (or pass them in)
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables.")

        # Initialize Auth Manager
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".spotify_cache",
            open_browser=False
        )

    def get_auth_url(self):
        """Returns the URL needed to authorize the user."""
        return self.sp_oauth.get_authorize_url()

    def handle_auth_code(self, code: str):
        """Exchanges the callback code for a permanent token."""
        return self.sp_oauth.get_access_token(code)

    def get_client(self):
        """
        Returns an authenticated spotipy client. 
        Refreshes token automatically if needed.
        """
        token_info = self.sp_oauth.get_cached_token()
        if not token_info:
            # If no token is cached, we cannot proceed.
            # In a real app, you might raise a specific exception to trigger a redirect.
            return None
        return spotipy.Spotify(auth=token_info['access_token'])

    # --- Actions ---

    def get_current_track(self):
        sp = self.get_client()
        if not sp: return None

        current = sp.current_playback()
        if not current or not current.get('item'):
            return None

        return {
            "track": current['item']['name'],
            "artist": ", ".join([artist['name'] for artist in current['item']['artists']]),
            "album": current['item']['album']['name'],
            "is_playing": current['is_playing'],
            "volume": current['device']['volume_percent'],
            "image": current['item']['album']['images'][0]['url'] if current['item']['album']['images'] else None
        }

    def play(self):
        sp = self.get_client()
        if sp: sp.start_playback()

    def pause(self):
        sp = self.get_client()
        if sp: sp.pause_playback()

    def next_track(self):
        sp = self.get_client()
        if sp: sp.next_track()

    def previous_track(self):
        sp = self.get_client()
        if sp: sp.previous_track()

    def set_volume(self, volume: int):
        sp = self.get_client()
        if sp: sp.volume(volume)
