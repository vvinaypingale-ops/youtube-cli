import socket
import speech_recognition as sr

try:
    import sounddevice as sd
    import numpy as np
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

class SpeechInput:
    """
    Multilingual microphone input supporting:
    en-IN (English), hi-IN (Hindi), kn-IN (Kannada), te-IN (Telugu),
    ta-IN (Tamil), ml-IN (Malayalam), bn-IN (Bengali), es-ES (Spanish), fr-FR (French).
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def is_online(self) -> bool:
        try:
            socket.create_connection(("www.google.com", 80), timeout=3)
            return True
        except Exception:
            return False

    def listen(self, language_code: str = "en-IN", duration: int = 5) -> str:
        """
        Listens to microphone input and converts speech to text.
        """
        if not self.is_online():
            print("❌ No internet connection found for speech recognition.")
            return None

        audio = None

        # 1. Try PyAudio microphone if available
        try:
            mic = sr.Microphone()
            with mic as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
        except Exception:
            # 2. Fallback to pre-compiled Windows sounddevice recording
            if HAS_SOUNDDEVICE:
                try:
                    sample_rate = 16000
                    print(f"🎤 Listening ({duration}s)...")
                    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
                    sd.wait()
                    audio = sr.AudioData(recording.tobytes(), sample_rate, 2)
                except Exception as e:
                    print(f"❌ Microphone input error: {e}")
                    return None
            else:
                print("❌ No microphone audio backend available.")
                return None

        if audio:
            try:
                text = self.recognizer.recognize_google(audio, language=language_code)
                print(f"🗣️ Heard: {text}")
                return text.strip()
            except sr.UnknownValueError:
                print("🪛 No clear speech detected.")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                return None

        return None
