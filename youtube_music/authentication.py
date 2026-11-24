import os
from youtube_music.client import get_ytmusic_client

def get_auth_status() -> dict:
    """
    Checks whether the YouTube Music client is running in an authenticated session.
    """
    auth_file = os.getenv("YTM_AUTH_FILE", "")
    for path in [auth_file, "oauth.json", "browser.json", "headers_auth.json"]:
        if path and os.path.exists(path):
            return {
                "authenticated": True,
                "auth_file": path,
                "mode": "OAuth / Browser Session",
                "can_manage_private_playlists": True
            }

    return {
        "authenticated": False,
        "auth_file": None,
        "mode": "Public Mode (No API keys or logins required)",
        "can_manage_private_playlists": False
    }

def print_auth_info():
    status = get_auth_status()
    print("\n🔐 YouTube Music Authentication Status:")
    print(f"  • Mode: {status['mode']}")
    print(f"  • Private Playlist Creation: {'Supported' if status['can_manage_private_playlists'] else 'Local DB & Web Queue Mode'}")
    if not status["authenticated"]:
        print("  💡 Tip: Public Mode gives full access to search, stream, artists, and playlists without any login.")
