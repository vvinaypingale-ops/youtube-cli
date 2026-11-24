import unittest
from ai_engine.response_generator import ResponseGenerator
from ai_engine.intent_parser import IntentParser
from ai_engine.intent_schema import IntentType
from youtube_music.search import YouTubeMusicSearch
from unittest.mock import MagicMock
import time

class TestAdvancedAIAndResponses(unittest.TestCase):
    def setUp(self):
        self.resp_gen = ResponseGenerator()
        self.parser = IntentParser()

    def test_multilingual_response_formatting(self):
        # English
        en_resp = self.resp_gen.format("en", "playing_track", title="Kesariya", artist="Arijit Singh")
        self.assertIn("Kesariya", en_resp)
        self.assertIn("Arijit Singh", en_resp)

        # Hindi
        hi_resp = self.resp_gen.format("hi", "playing_track", title="Kesariya", artist="Arijit Singh")
        self.assertIn("Kesariya", hi_resp)

        # Hinglish
        hing_resp = self.resp_gen.format("hinglish", "playing_artist", artist="Arijit Singh")
        self.assertIn("Arijit Singh", hing_resp)

        # Kannada
        kn_resp = self.resp_gen.format("kn", "playing_artist", artist="Vijay Prakash")
        self.assertIn("Vijay Prakash", kn_resp)

        # Telugu
        te_resp = self.resp_gen.format("te", "playing_artist", artist="Sid Sriram")
        self.assertIn("Sid Sriram", te_resp)

    def test_conversational_preamble_stripping(self):
        # "Can you please play Starboy"
        intent1 = self.parser.parse("Can you please play Starboy")
        self.assertEqual(intent1.intent, IntentType.PLAY_TRACK)
        self.assertEqual(intent1.song_title, "Starboy")

        # "I want to listen to Believer"
        intent2 = self.parser.parse("I want to listen to Believer")
        self.assertEqual(intent2.intent, IntentType.PLAY_TRACK)
        self.assertEqual(intent2.song_title, "Believer")

        # "Bhai mujhe Arijit Singh ke gaane sunao"
        intent3 = self.parser.parse("Bhai mujhe Arijit Singh ke gaane sunao")
        self.assertEqual(intent3.intent, IntentType.PLAY_ARTIST)
        self.assertEqual(intent3.artist, "Arijit Singh")

    def test_search_caching_speed(self):
        mock_yt = MagicMock()
        mock_yt.search.return_value = [{"title": "Test Song", "videoId": "v1", "artists": [{"name": "Test Artist"}]}]
        search = YouTubeMusicSearch(yt=mock_yt)

        # First call hits mock
        res1 = search.search_songs("Test Query", limit=1)
        self.assertEqual(len(res1), 1)
        self.assertEqual(mock_yt.search.call_count, 1)

        # Second call hits cache (0 mock calls)
        res2 = search.search_songs("Test Query", limit=1)
        self.assertEqual(len(res2), 1)
        self.assertEqual(mock_yt.search.call_count, 1)  # Cached!

if __name__ == "__main__":
    unittest.main()
