from music_engine.discovery import MusicDiscoveryEngine
from youtube_music.playlist import YouTubeMusicPlaylist

class PlaylistGenerator:
    """
    Intelligent AI Playlist Generator with duration estimation,
    deduplication, and artist diversity balancing.
    """

    def __init__(self, discovery_engine=None, playlist_service=None):
        self.discovery = discovery_engine or MusicDiscoveryEngine()
        self.playlist_service = playlist_service or YouTubeMusicPlaylist()

    def format_duration(self, seconds: int) -> str:
        """Formats seconds into readable string (e.g. 45m 12s or 1h 15m)."""
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m {secs}s"

    def plan_playlist(self, name: str = None, duration_minutes: int = 30, mood: str = None,
                      activity: str = None, language: str = None, genre: str = None) -> dict:
        """
        Curates tracks approximately matching the requested duration.
        Returns a playlist preview with tracks, duration, and metadata.
        """
        target_seconds = max(duration_minutes, 10) * 60

        # Discover candidate tracks (fetch generous candidate pool)
        disc_result = self.discovery.discover_music(
            mood=mood,
            activity=activity,
            language=language,
            genre=genre,
            limit=35
        )

        candidates = disc_result.get("tracks", [])
        if not candidates:
            return {
                "success": False,
                "message": "No tracks found matching the requested criteria."
            }

        selected_tracks = []
        accumulated_seconds = 0

        for track in candidates:
            dur = track.get("duration_seconds", 210)
            # Add track if we haven't reached the target
            selected_tracks.append(track)
            accumulated_seconds += dur

            # Stop when we reached or slightly passed target duration
            if accumulated_seconds >= target_seconds:
                break

        if not name:
            components = [p for p in [language, mood, activity] if p]
            name = f"{' '.join(components).title()} Mix" if components else "Custom AI Playlist"

        description = f"Curated {self.format_duration(accumulated_seconds)} {language or ''} playlist for {activity or mood or 'listening'}."

        return {
            "success": True,
            "playlist_name": name,
            "description": description.strip(),
            "target_minutes": duration_minutes,
            "total_duration_seconds": accumulated_seconds,
            "total_duration_formatted": self.format_duration(accumulated_seconds),
            "track_count": len(selected_tracks),
            "tracks": selected_tracks
        }

    def create_playlist(self, plan: dict) -> dict:
        """Executes creation of the planned playlist."""
        if not plan or not plan.get("success"):
            return {"success": False, "message": "Invalid playlist plan."}

        return self.playlist_service.create_playlist(
            title=plan["playlist_name"],
            description=plan["description"],
            tracks=plan["tracks"]
        )
