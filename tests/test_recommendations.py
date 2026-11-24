import unittest
from unittest.mock import MagicMock
from music_engine.mood_classifier import MoodClassifier
from music_engine.ranking import TrackRanker
from music_engine.discovery import MusicDiscoveryEngine

class TestRecommendations(unittest.TestCase):
    def setUp(self):
        self.classifier = MoodClassifier()
        self.mock_prefs = MagicMock()
        self.mock_feedback = MagicMock()
        self.ranker = TrackRanker(prefs=self.mock_prefs, feedback=self.mock_feedback)

    def test_mood_classifier(self):
        q, exp = self.classifier.get_query_and_explanation(activity="coding", language="English")
        self.assertIn("coding", q.lower())
        self.assertIn("English", q)
        self.assertIn("instrumental", q.lower())

        q2, exp2 = self.classifier.get_query_and_explanation(mood="energetic", activity="workout", language="Hindi")
        self.assertIn("workout", q2.lower())
        self.assertIn("Hindi", q2)

    def test_track_scoring_and_penalties(self):
        self.mock_prefs.get_favorite_artists.return_value = ["Arijit Singh"]
        self.mock_prefs.get_preferred_language.return_value = "Hindi"
        self.mock_feedback.is_liked.return_value = False
        self.mock_feedback.is_disliked.return_value = False

        track_fav = {"title": "Channa Mereya", "artist": "Arijit Singh", "video_id": "v1"}
        score_fav = self.ranker.score_track(track_fav, target_lang="Hindi")
        # 50 base + 25 fav artist + 15 preferred lang = 90
        self.assertEqual(score_fav, 90.0)

        # Disliked track penalty
        self.mock_feedback.is_disliked.return_value = True
        score_disliked = self.ranker.score_track(track_fav)
        self.assertEqual(score_disliked, -100.0)

    def test_artist_diversity(self):
        tracks = [
            {"title": "Song 1", "artist": "Artist A", "video_id": "v1"},
            {"title": "Song 2", "artist": "Artist A", "video_id": "v2"},
            {"title": "Song 3", "artist": "Artist A", "video_id": "v3"},
            {"title": "Song 4", "artist": "Artist B", "video_id": "v4"},
            {"title": "Song 5", "artist": "Artist C", "video_id": "v5"}
        ]
        self.mock_prefs.get_favorite_artists.return_value = []
        self.mock_feedback.is_disliked.return_value = False
        self.mock_feedback.is_liked.return_value = False

        ranked = self.ranker.rank_and_deduplicate(tracks, max_per_artist=2)
        # First 4 tracks should feature diverse artists, not 3 of Artist A consecutively
        top_4_artists = [t["artist"] for t in ranked[:4]]
        self.assertIn("Artist B", top_4_artists)
        self.assertIn("Artist C", top_4_artists)

    def test_discovery_engine(self):
        self.mock_feedback.is_disliked.return_value = False
        self.mock_feedback.is_liked.return_value = False
        mock_search = MagicMock()
        mock_search.search_songs.return_value = [
            {"title": "Track 1", "artist": "Artist 1", "video_id": "v1", "duration_seconds": 180},
            {"title": "Track 2", "artist": "Artist 2", "video_id": "v2", "duration_seconds": 210}
        ]
        discovery = MusicDiscoveryEngine(search_engine=mock_search, ranker=self.ranker)
        res = discovery.discover_music(mood="relaxing", language="Hindi", limit=2)
        self.assertEqual(res["count"], 2)
        self.assertTrue(len(res["tracks"]) == 2)
        self.assertIn("explanation", res)

if __name__ == "__main__":
    unittest.main()
