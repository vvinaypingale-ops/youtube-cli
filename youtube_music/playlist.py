import webbrowser
from youtube_music.client import get_ytmusic_client
from youtube_music.authentication import get_auth_status
from memory.feedback import FeedbackManager

class YouTubeMusicPlaylist:
    def __init__(self, yt=None):
        self.yt = yt or get_ytmusic_client()
        self.feedback = FeedbackManager()

    def get_playlist(self, url_or_id: str) -> dict:
        """Retrieves playlist metadata and all tracks."""
        playlist_id = url_or_id
        if "list=" in url_or_id:
            playlist_id = url_or_id.split("list=")[-1].split("&")[0]

        try:
            data = self.yt.get_playlist(playlist_id)
            title = data.get("title", "Untitled")
            author = data.get("author", {})
            author_name = author.get("name", "Unknown") if isinstance(author, dict) else str(author or "Unknown")
            raw_tracks = data.get("tracks", [])

            tracks = []
            for t in raw_tracks:
                v_id = t.get("videoId")
                if not v_id:
                    continue
                artists = t.get("artists", [])
                art_name = artists[0].get("name", "Unknown") if artists else "Unknown"
                tracks.append({
                    "title": t.get("title", "Unknown"),
                    "artist": art_name,
                    "video_id": v_id,
                    "duration": t.get("duration", "3:30"),
                    "duration_seconds": t.get("duration_seconds", 210)
                })

            return {
                "id": playlist_id,
                "title": title,
                "author": author_name,
                "track_count": len(tracks),
                "tracks": tracks,
                "url": f"https://music.youtube.com/playlist?list={playlist_id}"
            }
        except Exception as e:
            print(f"❌ Error retrieving playlist '{playlist_id}': {e}")
            return None

    def create_playlist(self, title: str, description: str, tracks: list) -> dict:
        """
        Creates a playlist.
        If authenticated with oauth.json/headers: creates a live YouTube Music playlist.
        If unauthenticated: stores locally in SQLite and generates a YouTube Multi-Video stream URL.
        """
        video_ids = [t["video_id"] if isinstance(t, dict) else t for t in tracks if t]
        total_seconds = sum(t.get("duration_seconds", 210) for t in tracks if isinstance(t, dict))

        auth = get_auth_status()
        if auth["authenticated"]:
            try:
                playlist_id = self.yt.create_playlist(title, description, privacy_status="PRIVATE", video_ids=video_ids)
                pl_url = f"https://music.youtube.com/playlist?list={playlist_id}"
                self.feedback.record_playlist(title, description, total_seconds, len(video_ids), video_ids)
                return {
                    "success": True,
                    "id": playlist_id,
                    "title": title,
                    "url": pl_url,
                    "type": "Remote YouTube Music Playlist",
                    "track_count": len(video_ids),
                    "duration_seconds": total_seconds
                }
            except Exception as e:
                print(f"⚠️ Remote playlist creation failed ({e}); falling back to local playlist.")

        # Local SQLite curation + YouTube Multi-Video queue URL
        self.feedback.record_playlist(title, description, total_seconds, len(video_ids), video_ids)
        queue_url = f"https://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"

        return {
            "success": True,
            "id": f"local_{int(total_seconds)}",
            "title": title,
            "url": queue_url,
            "type": "Local Curated Queue (Saved in MUSIQ AI memory)",
            "track_count": len(video_ids),
            "duration_seconds": total_seconds
        }

    def open_playlist(self, url: str):
        print(f"▶️ Opening playlist stream: {url}")
        webbrowser.open(url)
