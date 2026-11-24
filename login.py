from youtube_music.client import get_ytmusic_client

def login():
    """Backward-compatible login function for legacy callers."""
    try:
        yt = get_ytmusic_client()
        print("✅ Connected to YouTube Music successfully")
        return {
            "access_token": "yt_active_session",
            "sp": yt,
            "yt": yt
        }
    except Exception as e:
        print(f"Error connecting to YouTube Music: {e}")
        return None

if __name__ == "__main__":
    login()
