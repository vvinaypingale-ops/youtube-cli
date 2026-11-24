import unittest
from ai_engine.intent_parser import IntentParser
from ai_engine.intent_schema import IntentType
from ai_engine.conversation_manager import ConversationManager

class TestIntentParser(unittest.TestCase):
    def setUp(self):
        self.parser = IntentParser()
        self.conv = ConversationManager()

    def test_play_track(self):
        intent = self.parser.parse("Play Rolling in the Deep")
        self.assertEqual(intent.intent, IntentType.PLAY_TRACK)
        self.assertEqual(intent.song_title, "Rolling in the Deep")

    def test_play_artist_multilingual(self):
        # Hinglish request
        intent = self.parser.parse("Mujhe Arijit Singh ke gaane sunne hain")
        self.assertEqual(intent.intent, IntentType.PLAY_ARTIST)
        self.assertEqual(intent.artist, "Arijit Singh")

    def test_kannada_mood_and_activity(self):
        intent = self.parser.parse("Nanage workout ge energetic songs beku")
        self.assertEqual(intent.intent, IntentType.MOOD_RECOMMENDATION)
        self.assertEqual(intent.activity, "workout")
        self.assertEqual(intent.mood, "energetic")

    def test_telugu_peaceful_music(self):
        intent = self.parser.parse("Naaku peaceful music play cheyyi")
        self.assertEqual(intent.intent, IntentType.MOOD_RECOMMENDATION)
        self.assertEqual(intent.mood, "peaceful")

    def test_hinglish_coding_instrumental(self):
        intent = self.parser.parse("Bhai coding ke liye kuch instrumental music chalao")
        self.assertEqual(intent.intent, IntentType.MOOD_RECOMMENDATION)
        self.assertEqual(intent.activity, "coding")
        self.assertEqual(intent.genre, "instrumental")

    def test_create_playlist_duration_extraction(self):
        intent = self.parser.parse("Create a 45-minute Hindi playlist for a relaxing evening")
        self.assertEqual(intent.intent, IntentType.CREATE_PLAYLIST)
        self.assertEqual(intent.duration_minutes, 45)
        self.assertEqual(intent.language, "Hindi")
        self.assertEqual(intent.mood, "relaxing")
        self.assertTrue(intent.requires_confirmation)

    def test_playback_controls(self):
        self.assertEqual(self.parser.parse("Pause the music").intent, IntentType.PAUSE)
        self.assertEqual(self.parser.parse("Skip this song").intent, IntentType.NEXT_TRACK)
        self.assertEqual(self.parser.parse("Resume music").intent, IntentType.RESUME)
        self.assertEqual(self.parser.parse("What am I listening to?").intent, IntentType.CURRENTLY_PLAYING)

    def test_multiturn_clarification_merge(self):
        # Turn 1: vague request
        intent1 = self.parser.parse("Play relaxing music")
        self.conv.pending_intent = intent1

        # Turn 2: user specifies language
        merged = self.conv.handle_followup_or_merge("Kannada", self.parser.parse("Kannada"))
        self.assertEqual(merged.language, "Kannada")
        self.assertEqual(merged.mood, "relaxing")

    def test_multiturn_confirmation(self):
        # Pending playlist action
        self.conv.set_pending_confirmation(
            action="CREATE_PLAYLIST",
            data={"playlist_name": "Workout Mix", "duration_minutes": 30},
            prompt="Should I create this playlist?"
        )
        # User confirms: "haan" / "yes"
        confirmed_intent = self.conv.handle_followup_or_merge("Haan create kar do", self.parser.parse("Haan create kar do"))
        self.assertEqual(confirmed_intent.intent, IntentType.CREATE_PLAYLIST)
        self.assertEqual(confirmed_intent.playlist_name, "Workout Mix")

if __name__ == "__main__":
    unittest.main()
