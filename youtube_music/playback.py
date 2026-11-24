import time
import webbrowser
import threading
import ctypes
from youtube_music.search import YouTubeMusicSearch

class YouTubeMusicPlayback:
    def __init__(self, search_engine=None):
        self.search = search_engine or YouTubeMusicSearch()
        self.current_track = None
        self.is_paused = False

    def play_track(self, query_or_track):
        """
        Plays a track by search query or pre-fetched track dict.
        Launches standard browser stream and updates internal state.
        """
        if isinstance(query_or_track, dict) and "video_id" in query_or_track:
            track = query_or_track
        else:
            tracks = self.search.search_songs(str(query_or_track), limit=1)
            if not tracks:
                print(f"❌ Could not find track for '{query_or_track}'")
                return None
            track = tracks[0]

        video_id = track.get("video_id") or track.get("videoId")
        stream_url = f"https://music.youtube.com/watch?v={video_id}"

        self.current_track = {
            "title": track.get("title") or track.get("name"),
            "artist": track.get("artist"),
            "video_id": video_id,
            "duration_seconds": track.get("duration_seconds", 210),
            "duration": track.get("duration", "3:30"),
            "start_time": time.time(),
            "url": stream_url
        }
        self.is_paused = False

        print(f"▶️ Playing: {self.current_track['title']} by {self.current_track['artist']}")
        print(f"🌐 Stream: {stream_url}")

        try:
            threading.Thread(target=webbrowser.open, args=(stream_url,), daemon=True).start()
        except Exception as e:
            print(f"⚠️ Browser open failed: {e}")

        return self.current_track

    def pause(self):
        """Sends global Windows media Play/Pause toggle key."""
        try:
            # VK_MEDIA_PLAY_PAUSE = 0xB3
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            self.is_paused = True
            print("⏸️ Playback paused / toggled.")
            return True
        except Exception as e:
            print(f"Error toggling media key: {e}")
            return False

    def resume(self):
        """Resumes playback using system media key."""
        try:
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            self.is_paused = False
            print("▶️ Playback resumed.")
            return True
        except Exception as e:
            print(f"Error resuming media key: {e}")
            return False

    def next_track(self):
        """Skips to next track using system media key."""
        try:
            # VK_MEDIA_NEXT_TRACK = 0xB0
            ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)
            print("⏭️ Skipped to next track.")
            return True
        except Exception as e:
            print(f"Error skipping track: {e}")
            return False

    def previous_track(self):
        """Returns to previous track using system media key."""
        try:
            # VK_MEDIA_PREV_TRACK = 0xB1
            ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)
            print("⏮️ Returned to previous track.")
            return True
        except Exception as e:
            print(f"Error returning to previous track: {e}")
            return False

    def get_current_playing(self) -> dict:
        """Returns current track metadata and live progress for TUI/CLI."""
        if not self.current_track:
            return None

        elapsed = int(time.time() - self.current_track["start_time"])
        duration = self.current_track["duration_seconds"]
        progress = min(elapsed, duration)

        return {
            "track": self.current_track["title"],
            "title": self.current_track["title"],
            "artist": self.current_track["artist"],
            "video_id": self.current_track["video_id"],
            "progress": progress,
            "duration": duration,
            "url": self.current_track["url"],
            "is_paused": self.is_paused
        }
