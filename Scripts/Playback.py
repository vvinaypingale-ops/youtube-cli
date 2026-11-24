from youtube_music.playback import YouTubeMusicPlayback
from youtube_music.search import YouTubeMusicSearch

class Playback:
    """Backward-compatible wrapper for YouTubeMusicPlayback."""
    def __init__(self, access_token=None, yt=None):
        self.playback = YouTubeMusicPlayback()
        self.search = self.playback.search

    def search_track(self, track_name, use_fuzzy=True, search_limit=10):
        tracks = self.search.search_songs(track_name, limit=search_limit)
        return tracks[0] if tracks else None

    def play(self, song_name):
        return self.playback.play_track(song_name)

    def pause(self):
        return self.playback.pause()

    def get_current_playing(self):
        return self.playback.get_current_playing()

    def play_playlist(self, url_or_name):
        pass
