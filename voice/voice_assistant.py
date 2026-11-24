import time
from voice.speech_input import SpeechInput
from voice.speech_output import SpeechOutput
from ai_engine.language_detector import LanguageDetector
from ai_engine.intent_parser import IntentParser
from ai_engine.intent_schema import IntentType
from ai_engine.conversation_manager import ConversationManager
from youtube_music.playback import YouTubeMusicPlayback
from youtube_music.search import YouTubeMusicSearch
from music_engine.discovery import MusicDiscoveryEngine
from music_engine.playlist_generator import PlaylistGenerator
from memory.user_preferences import UserPreferencesManager

class VoiceAssistant:
    """
    Multilingual Voice Assistant pipeline:
    Microphone -> Speech Recognition -> Language Detection ->
    AI Intent Processing -> Validation -> Service Dispatcher -> Speech Output.
    """

    def __init__(self):
        self.speech_in = SpeechInput()
        self.speech_out = SpeechOutput()
        self.detector = LanguageDetector()
        self.parser = IntentParser()
        self.conv = ConversationManager()
        self.search = YouTubeMusicSearch()
        self.playback = YouTubeMusicPlayback(self.search)
        self.discovery = MusicDiscoveryEngine(self.search)
        self.generator = PlaylistGenerator(self.discovery)
        self.prefs = UserPreferencesManager()

        self.active = False
        self.last_activity = time.time()
        self.timeout = 20

    def run_loop(self):
        """Main listening and execution loop."""
        print("\n🎤 MUSIQ AI Voice Assistant Ready.")
        print("💡 Say 'Hello' or speak your command directly. Say 'Exit' to quit.")

        # Determine speech recognition language from stored preferences
        pref_lang = self.prefs.get_preferred_language("en")
        speech_code = self.detector.get_speech_recognition_code(pref_lang)

        while True:
            try:
                raw_text = self.speech_in.listen(language_code=speech_code, duration=5)
                if not raw_text:
                    if self.active and (time.time() - self.last_activity > self.timeout):
                        print("💤 Going to sleep... Say 'Hello' to wake me.")
                        self.active = False
                    continue

                low = raw_text.lower().strip()
                if low in ["exit", "quit", "bye", "band karo"]:
                    self.speech_out.speak("Goodbye! Enjoy your music.")
                    break

                # Wake-word activation
                if not self.active:
                    if any(w in low for w in ["hello", "namaste", "namaskara", "musiq", "hey"]):
                        self.active = True
                        self.last_activity = time.time()
                        self.speech_out.speak("Hello! I am listening. What music would you like to hear?")
                        continue

                self.last_activity = time.time()
                self.active = True

                # Process command
                self.dispatch_voice_command(raw_text)

            except KeyboardInterrupt:
                print("\n👋 Voice assistant stopped.")
                break
            except Exception as e:
                print(f"⚠️ Voice loop error: {e}")

    def dispatch_voice_command(self, text: str):
        # 1. Detect language
        detected_lang = self.detector.detect_language(text)

        # 2. Parse Intent with validation
        intent = self.parser.parse(text)
        intent = self.conv.handle_followup_or_merge(text, intent)

        # 3. Dispatch to service
        if intent.intent == IntentType.PLAY_TRACK:
            query = intent.song_title or intent.query or text
            self.speech_out.speak(f"Playing '{query}' on YouTube Music.")
            self.playback.play_track(query)

        elif intent.intent == IntentType.PLAY_ARTIST:
            artist = intent.artist or intent.query
            self.speech_out.speak(f"Playing top songs by {artist}.")
            self.playback.play_track(f"{artist} top songs")

        elif intent.intent == IntentType.MOOD_RECOMMENDATION:
            disc = self.discovery.discover_music(
                mood=intent.mood,
                activity=intent.activity,
                language=intent.language,
                genre=intent.genre,
                limit=5
            )
            tracks = disc.get("tracks", [])
            if tracks:
                top_track = tracks[0]
                self.speech_out.speak(f"Found {disc.get('explanation', 'tracks')}. Playing '{top_track['title']}' by {top_track['artist']}.")
                self.playback.play_track(top_track)
            else:
                self.speech_out.speak("I could not find matching tracks. Try another mood or artist.")

        elif intent.intent == IntentType.PAUSE:
            self.playback.pause()
            self.speech_out.speak("Paused playback.")

        elif intent.intent == IntentType.RESUME:
            self.playback.resume()
            self.speech_out.speak("Resumed playback.")

        elif intent.intent == IntentType.NEXT_TRACK:
            self.playback.next_track()
            self.speech_out.speak("Skipping to next track.")

        elif intent.intent == IntentType.PREVIOUS_TRACK:
            self.playback.previous_track()
            self.speech_out.speak("Returning to previous track.")

        elif intent.intent == IntentType.CURRENTLY_PLAYING:
            curr = self.playback.get_current_playing()
            if curr:
                self.speech_out.speak(f"Currently playing: {curr['title']} by {curr['artist']}.")
            else:
                self.speech_out.speak("Nothing is currently playing.")

        elif intent.intent == IntentType.CREATE_PLAYLIST:
            plan = self.generator.plan_playlist(
                name=intent.playlist_name,
                duration_minutes=intent.duration_minutes or 30,
                mood=intent.mood,
                activity=intent.activity,
                language=intent.language
            )
            if plan.get("success"):
                res = self.generator.create_playlist(plan)
                self.speech_out.speak(f"Created playlist '{plan['playlist_name']}' with {plan['track_count']} songs lasting {plan['total_duration_formatted']}.")
                self.playback.play_track(plan["tracks"][0])
            else:
                self.speech_out.speak("Could not create playlist.")

        else:
            prompt = intent.clarification_prompt or "Could you clarify what music you would like to hear?"
            self.speech_out.speak(prompt)
