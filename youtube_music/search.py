import time
from functools import lru_cache
from youtube_music.client import get_ytmusic_client

class YouTubeMusicSearch:
    def __init__(self, yt=None):
        self.yt = yt or get_ytmusic_client()
        self._cache = {}
        self._cache_ttl = 600  # 10 minutes cache

    def search_songs(self, query: str, limit: int = 10) -> list:
        """
        Searches YouTube Music for tracks matching the query.
        Uses in-memory caching to eliminate redundant network latency.
        """
        if not query or not query.strip():
            return []

        q = query.strip()
        cache_key = f"songs_{q}_{limit}"
        now = time.time()

        if cache_key in self._cache:
            entry_time, data = self._cache[cache_key]
            if now - entry_time < self._cache_ttl:
                return data

        try:
            results = self.yt.search(q, filter="songs")
            if not results:
                results = self.yt.search(q, filter="videos")

            tracks = []
            for item in results[:limit]:
                artists = item.get("artists", [])
                artist_name = artists[0].get("name", "Unknown") if artists else "Unknown"
                video_id = item.get("videoId")
                if not video_id:
                    continue

                duration_str = item.get("duration", "3:30")
                duration_sec = item.get("duration_seconds")
                if duration_sec is None:
                    try:
                        parts = [int(p) for p in str(duration_str).split(":")]
                        duration_sec = parts[0] * 60 + parts[1] if len(parts) == 2 else 210
                    except Exception:
                        duration_sec = 210

                thumbs = item.get("thumbnails", [])
                thumbnail_url = thumbs[-1].get("url") if thumbs else None

                tracks.append({
                    "title": item.get("title", "Unknown Track"),
                    "name": item.get("title", "Unknown Track"),
                    "artist": artist_name,
                    "artists": [a.get("name", "") for a in artists] if artists else [artist_name],
                    "video_id": video_id,
                    "videoId": video_id,
                    "duration": duration_str,
                    "duration_seconds": duration_sec,
                    "album": item.get("album", {}).get("name") if isinstance(item.get("album"), dict) else None,
                    "thumbnail": thumbnail_url,
                    "views": item.get("views"),
                    "url": f"https://music.youtube.com/watch?v={video_id}"
                })

            self._cache[cache_key] = (now, tracks)
            return tracks
        except Exception as e:
            print(f"❌ Error searching YouTube Music for '{query}': {e}")
            return []

    def search_artists(self, query: str, limit: int = 5) -> list:
        """
        Fast artist search without sequential blocking get_artist() HTTP requests.
        """
        q = query.strip()
        cache_key = f"artists_{q}_{limit}"
        now = time.time()

        if cache_key in self._cache:
            entry_time, data = self._cache[cache_key]
            if now - entry_time < self._cache_ttl:
                return data

        try:
            results = self.yt.search(q, filter="artists")
            artists = []
            for item in results[:limit]:
                browse_id = item.get("browseId")
                name = item.get("artist") or item.get("name") or "Unknown"

                # Extract subscribers from search result directly if present
                subscribers = item.get("subscribers") or item.get("itemCount") or "YouTube Artist"

                thumbs = item.get("thumbnails", [])
                thumbnail = thumbs[-1].get("url") if thumbs else None

                artists.append({
                    "name": name,
                    "browse_id": browse_id,
                    "subscribers": subscribers,
                    "thumbnail": thumbnail,
                    "url": f"https://music.youtube.com/channel/{browse_id}" if browse_id else None
                })

            # Fetch top artist detailed subscriber count once if browse_id available
            if artists and artists[0]["browse_id"] and artists[0]["subscribers"] == "YouTube Artist":
                try:
                    info = self.yt.get_artist(artists[0]["browse_id"])
                    if info.get("subscribers"):
                        artists[0]["subscribers"] = info.get("subscribers")
                except Exception:
                    pass

            self._cache[cache_key] = (now, artists)
            return artists
        except Exception as e:
            print(f"❌ Error searching artists for '{query}': {e}")
            return []

    def search_playlists(self, query: str, limit: int = 5) -> list:
        """Searches YouTube Music for playlists with caching."""
        q = query.strip()
        cache_key = f"playlists_{q}_{limit}"
        now = time.time()

        if cache_key in self._cache:
            entry_time, data = self._cache[cache_key]
            if now - entry_time < self._cache_ttl:
                return data

        try:
            results = self.yt.search(q, filter="playlists")
            playlists = []
            for item in results[:limit]:
                thumbs = item.get("thumbnails", [])
                thumbnail = thumbs[-1].get("url") if thumbs else None
                author = item.get("author", "YouTube Music")
                if isinstance(author, dict):
                    author = author.get("name", "YouTube Music")

                playlists.append({
                    "title": item.get("title", "Untitled"),
                    "name": item.get("title", "Untitled"),
                    "browse_id": item.get("browseId"),
                    "item_count": item.get("itemCount"),
                    "author": author,
                    "thumbnail": thumbnail,
                    "url": f"https://music.youtube.com/playlist?list={item.get('browseId')}"
                })

            self._cache[cache_key] = (now, playlists)
            return playlists
        except Exception as e:
            print(f"❌ Error searching playlists for '{query}': {e}")
            return []

    def search_albums(self, query: str, limit: int = 5) -> list:
        """Searches YouTube Music for albums."""
        try:
            results = self.yt.search(query, filter="albums")
            albums = []
            for item in results[:limit]:
                artists = item.get("artists", [])
                artist_name = artists[0].get("name", "Unknown") if artists else "Unknown"
                albums.append({
                    "title": item.get("title", "Untitled Album"),
                    "artist": artist_name,
                    "browse_id": item.get("browseId"),
                    "year": item.get("year"),
                    "url": f"https://music.youtube.com/browse/{item.get('browseId')}"
                })
            return albums
        except Exception as e:
            print(f"❌ Error searching albums for '{query}': {e}")
            return []
