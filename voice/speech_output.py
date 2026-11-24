import subprocess
import threading
import re

class SpeechOutput:
    """
    Handles speech synthesis and spoken responses.
    Outputs to terminal with optional non-blocking native Windows TTS.
    """

    def __init__(self, enable_tts: bool = True):
        self.enable_tts = enable_tts

    def speak(self, text: str, language: str = "en"):
        """
        Displays spoken response and plays audio if enabled.
        """
        if not text:
            return

        print(f"\n🤖 MUSIQ AI: {text}")

        if self.enable_tts:
            threading.Thread(target=self._speak_async, args=(text,), daemon=True).start()

    def _speak_async(self, text: str):
        try:
            # Clean text for speech synthesis
            clean = re.sub(r"[^\w\s\.,!\?]", "", text).strip()
            if not clean:
                return

            cmd = [
                "powershell", "-NoProfile", "-Command",
                f"(New-Object -ComObject SAPI.SpVoice).Speak('{clean}')"
            ]
            subprocess.run(cmd, capture_output=True, timeout=10)
        except Exception:
            pass
