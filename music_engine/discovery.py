from youtube_music.search import YouTubeMusicSearch
from music_engine.mood_classifier import MoodClassifier
from music_engine.ranking import TrackRanker

class MusicDiscoveryEngine:
    """
    Intelligent Music Discovery combining mood classification,
    content-based search, preference scoring, and diversity ranking.
    """

    def __init__(self, search_engine=None, ranker=None):
        self.search = search_engine or YouTubeMusicSearch()
        self.classifier = MoodClassifier()
        self.ranker = ranker or TrackRanker()

    def discover_music(self, mood: str = None, activity: str = None, language: str = None,
                       genre: str = None, artist: str = None, limit: int = 10) -> dict:
        """
        Discovers tracks based on multidimensional context.
        """
        if artist:
            query = f"{artist} top songs"
            explanation = f"Curated popular songs by {artist}."
        else:
            query, explanation = self.classifier.get_query_and_explanation(
                mood=mood,
                activity=activity,
                language=language
            )
            if genre:
                query = f"{genre} {query}"

        # Fetch candidate tracks from YouTube Music
        raw_candidates = self.search.search_songs(query, limit=max(limit * 2, 20))
        if not raw_candidates and language:
            # Fallback to broader language query
            raw_candidates = self.search.search_songs(f"{language} hits", limit=15)

        # Rank and deduplicate
        ranked = self.ranker.rank_and_deduplicate(
            raw_candidates,
            max_per_artist=2,
            target_artist=artist
        )

        selected = ranked[:limit]
        return {
            "query": query,
            "explanation": explanation,
            "count": len(selected),
            "tracks": selected
        }

    def find_similar(self, artist_or_song: str, limit: int = 10) -> dict:
        """
        Finds music similar to a target artist or song.
        """
        query = f"songs similar to {artist_or_song}"
        candidates = self.search.search_songs(query, limit=limit * 2)
        ranked = self.ranker.rank_and_deduplicate(candidates, max_per_artist=2)
        selected = ranked[:limit]

        return {
            "query": query,
            "target": artist_or_song,
            "explanation": f"Tracks sharing stylistic and acoustic similarity with {artist_or_song}.",
            "count": len(selected),
            "tracks": selected
        }
