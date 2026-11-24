import unittest
from ai_engine.language_detector import LanguageDetector

class TestMultilingualDetection(unittest.TestCase):
    def setUp(self):
        self.detector = LanguageDetector()

    def test_native_scripts(self):
        # Hindi Devanagari
        self.assertEqual(self.detector.detect_language("मुझे अरिजीत सिंह के गाने सुनने हैं"), "hi")
        # Kannada script
        self.assertEqual(self.detector.detect_language("ನನಗೆ ಹಾಡುಗಳು ಬೇಕು"), "kn")
        # Telugu script
        self.assertEqual(self.detector.detect_language("నాకు పాటలు కావాలి"), "te")
        # Tamil script
        self.assertEqual(self.detector.detect_language("எனக்கு பாடல் வேண்டும்"), "ta")
        # Bengali script
        self.assertEqual(self.detector.detect_language("আমাকে গান শোনাও"), "bn")

    def test_romanized_code_switching(self):
        # Hinglish
        self.assertEqual(self.detector.detect_language("Bhai coding ke liye kuch gaane chalao"), "hinglish")
        self.assertEqual(self.detector.detect_language("Mujhe Arijit Singh ke gaane sunne hain"), "hinglish")
        # Kannada-English
        self.assertEqual(self.detector.detect_language("Nanage workout ge energetic songs beku"), "kannada-english")
        # Telugu-English
        self.assertEqual(self.detector.detect_language("Naaku peaceful music play cheyyi"), "telugu-english")
        # Tamil-English
        self.assertEqual(self.detector.detect_language("Enakku coding panna instrumental music venum"), "tamil-english")

    def test_european_languages(self):
        # Spanish
        self.assertEqual(self.detector.detect_language("Reproducir musica relajante para dormir"), "es")
        # French
        self.assertEqual(self.detector.detect_language("Jouer de la musique calme pour dormir"), "fr")

    def test_english(self):
        self.assertEqual(self.detector.detect_language("Play something relaxing"), "en")
        self.assertEqual(self.detector.detect_language("Create a 30-minute workout playlist"), "en")

    def test_bcp47_mapping(self):
        self.assertEqual(self.detector.get_speech_recognition_code("hi"), "hi-IN")
        self.assertEqual(self.detector.get_speech_recognition_code("kn"), "kn-IN")
        self.assertEqual(self.detector.get_speech_recognition_code("te"), "te-IN")
        self.assertEqual(self.detector.get_speech_recognition_code("ta"), "ta-IN")
        self.assertEqual(self.detector.get_speech_recognition_code("es"), "es-ES")

if __name__ == "__main__":
    unittest.main()
