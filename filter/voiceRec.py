import speech_recognition as sr
import socket

try:
    import sounddevice as sd
    import numpy as np
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

def isOnline():
    try:
        socket.create_connection(("www.google.com", 80), timeout=3)
        return True
    except Exception:
        return False

def record_via_sounddevice(r, duration=4, sample_rate=16000):
    print("🎤 Listening (4s)...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return sr.AudioData(recording.tobytes(), sample_rate, 2)

def audioRec():
    if not isOnline():
        print("❌ No Internet connection found.")
        return None

    r = sr.Recognizer()
    audio = None

    # Try PyAudio microphone first, fallback to sounddevice
    try:
        mic = sr.Microphone()
        with mic as source:
            print("🎤 Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
    except Exception:
        if HAS_SOUNDDEVICE:
            try:
                audio = record_via_sounddevice(r, duration=4)
            except Exception as e:
                print(f"❌ Microphone recording error: {e}")
                return None
        else:
            print("❌ No microphone audio backend available.")
            return None

    if audio:
        try:
            inp = r.recognize_google(audio)
            print(f"🗣️ Heard: {inp}")
            lst_out = inp.split(" ", 1)
            return lst_out if len(lst_out) > 0 else None
        except sr.UnknownValueError:
            print("🪛 No clear speech detected.")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            return None

    return None
