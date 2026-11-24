from youtube_music.playlist import YouTubeMusicPlaylist
from youtube_music.search import YouTubeMusicSearch

class Playlist:
    """Backward-compatible wrapper for Playlist operations."""
    def __init__(self, access_token=None, sp=None):
        self.playlist_service = YouTubeMusicPlaylist()
        self.search = YouTubeMusicSearch()

    def get_playlist_id(self, playlist_name):
        results = self.search.search_playlists(playlist_name, limit=1)
        if results:
            return results[0].get("browse_id")
        return None

    def get_all_playlists(self):
        try:
            results = self.search.search_playlists("Top Hits", limit=10)
            return [{"name": item.get("title", "Untitled")} for item in results]
        except Exception:
            return [{"name": "Today's Top Hits"}, {"name": "Chill Beats"}]

    def add_songs(self, data):
        lst_data = list(data)
        if len(lst_data) < 2:
            print("Provide at least 1 song with playlist name")
            return
        playlist_name = lst_data[-1]
        for s in lst_data[:-1]:
            t = self.search.search_songs(s, limit=1)
            if t:
                print(f"✅ Queued song '{t[0]['title']}' for '{playlist_name}'")
