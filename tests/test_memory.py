import os
import unittest
import tempfile
from pathlib import Path

class TestMemoryLayer(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for isolation during testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        os.environ["MUSIQ_DB_PATH"] = self.temp_db.name

        from memory.database import init_db
        init_db()

        from memory.user_preferences import UserPreferencesManager
        from memory.feedback import FeedbackManager
        self.prefs = UserPreferencesManager()
        self.feedback = FeedbackManager()

    def tearDown(self):
        os.environ.pop("MUSIQ_DB_PATH", None)
        try:
            os.remove(self.temp_db.name)
        except Exception:
            pass

    def test_language_preference(self):
        self.assertEqual(self.prefs.get_preferred_language(), "en")
        self.prefs.set_preferred_language("hi")
        self.assertEqual(self.prefs.get_preferred_language(), "hi")
        self.prefs.set_preferred_language("kn")
        self.assertEqual(self.prefs.get_preferred_language(), "kn")

    def test_favorite_artists(self):
        self.assertEqual(self.prefs.get_favorite_artists(), [])
        self.prefs.add_favorite_artist("Arijit Singh")
        self.prefs.add_favorite_artist("Vijay Prakash")
        self.assertIn("Arijit Singh", self.prefs.get_favorite_artists())
        self.assertIn("Vijay Prakash", self.prefs.get_favorite_artists())

        self.prefs.remove_favorite_artist("Arijit Singh")
        self.assertNotIn("Arijit Singh", self.prefs.get_favorite_artists())
        self.assertIn("Vijay Prakash", self.prefs.get_favorite_artists())

    def test_activity_preference(self):
        self.prefs.set_activity_preference("coding", genre="instrumental", mood="focus", language="any")
        act = self.prefs.get_activity_preference("coding")
        self.assertEqual(act.get("genre"), "instrumental")
        self.assertEqual(act.get("mood"), "focus")

        self.prefs.set_activity_preference("workout", genre="edm", mood="energetic", language="any")
        act_workout = self.prefs.get_activity_preference("workout")
        self.assertEqual(act_workout.get("mood"), "energetic")

    def test_track_feedback(self):
        self.feedback.record_like("Believer", "Imagine Dragons", "videoId_123")
        self.assertTrue(self.feedback.is_liked("Believer", "Imagine Dragons"))
        self.assertFalse(self.feedback.is_disliked("Believer", "Imagine Dragons"))

        self.feedback.record_dislike("Baby", "Justin Bieber", "videoId_456")
        self.assertTrue(self.feedback.is_disliked("Baby", "Justin Bieber"))
        self.assertFalse(self.feedback.is_liked("Baby", "Justin Bieber"))

    def test_playlist_history(self):
        self.feedback.record_playlist("Evening Chill", "Relaxing acoustic", 1800, 10, ["v1", "v2", "v3"])
        history = self.feedback.get_playlist_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["playlist_name"], "Evening Chill")
        self.assertEqual(history[0]["track_count"], 10)
        self.assertEqual(history[0]["video_ids"], ["v1", "v2", "v3"])

if __name__ == "__main__":
    unittest.main()
