import os
from pathlib import Path
from ytmusicapi import YTMusic

_client_instance = None

def get_ytmusic_client() -> YTMusic:
    """
    Returns a singleton instance of YTMusic.
    Attempts to load an authenticated session if credentials exist,
    otherwise falls back gracefully to standard public access.
    """
    global _client_instance
    if _client_instance is not None:
        return _client_instance

    auth_file = os.getenv("YTM_AUTH_FILE", "")
    possible_paths = [
        auth_file,
        "oauth.json",
        "browser.json",
        "headers_auth.json",
        ".yt_session.json"
    ]

    for path in possible_paths:
        if path and os.path.exists(path):
            try:
                _client_instance = YTMusic(path)
                return _client_instance
            except Exception:
                pass

    # Public unauthenticated client (full search, artist info, playlist access)
    _client_instance = YTMusic()
    return _client_instance

def reset_ytmusic_client():
    global _client_instance
    _client_instance = None
