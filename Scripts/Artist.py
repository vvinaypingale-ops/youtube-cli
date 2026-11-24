from youtube_music.search import YouTubeMusicSearch

class Artist:
    """Backward-compatible wrapper for Artist search."""
    def __init__(self, access_token=None, yt=None):
        self.search = YouTubeMusicSearch()

    def artist_name(self, name):
        results = self.search.search_artists(name, limit=5)
        if results:
            print(f"\n🔍 Search Results:")
            for a in results:
                print(f"🎤 {a['name']} | Subscribers: {a['subscribers']}")
                if a.get('url'):
                    print(f"   🌐 {a['url']}")
        else:
            print("No artist found.")
