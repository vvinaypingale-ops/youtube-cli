import re

class LanguageDetector:
    """
    Multilingual detector supporting:
    - English (en)
    - Hindi (hi & Hinglish)
    - Kannada (kn & Kannada-English)
    - Telugu (te & Telugu-English)
    - Tamil (ta & Tamil-English)
    - Malayalam (ml & Malayalam-English)
    - Bengali (bn & Bengali-English)
    - Spanish (es)
    - French (fr)
    """

    # Unicode script ranges
    SCRIPT_RANGES = {
        "hi": re.compile(r"[\u0900-\u097F]"),  # Devanagari
        "bn": re.compile(r"[\u0980-\u09FF]"),  # Bengali
        "ta": re.compile(r"[\u0B80-\u0BFF]"),  # Tamil
        "te": re.compile(r"[\u0C00-\u0C7F]"),  # Telugu
        "kn": re.compile(r"[\u0C80-\u0CFF]"),  # Kannada
        "ml": re.compile(r"[\u0D00-\u0D7F]"),  # Malayalam
    }

    # Romanized keyword lexicons for code-switching
    ROMAN_LEXICONS = {
        "hinglish": {
            "bhai", "gaane", "gaana", "sunna", "sunne", "chalao", "bajao", "kuch",
            "mujhe", "chahiye", "liye", "aur", "thoda", "mast", "badhiya", "lagao"
        },
        "kannada-english": {
            "nanage", "beku", "haadu", "haadugalu", "kelabeku", "maadi", "yavudu",
            "haadi", "hosa", "nodona", "kodu", "ge"
        },
        "telugu-english": {
            "naaku", "cheyyi", "paatalu", "paata", "kavali", "veeyi", "vinali",
            "vinadaniki", "manchi"
        },
        "tamil-english": {
            "enakku", "venum", "paattu", "podu", "kelu", "kekkalam", "nalla",
            "vidham", "panna"
        },
        "malayalam-english": {
            "enikku", "paattukal", "paattu", "venam", "kelkkanam", "nalla"
        },
        "bengali-english": {
            "aamar", "gaan", "shunte", "chai", "bajao", "shunbo"
        },
        "es": {
            "musica", "cancion", "canciones", "reproducir", "para", "relajante",
            "dormir", "entrenar", "estudiar", "favorito", "pausa"
        },
        "fr": {
            "musique", "chanson", "chansons", "jouer", "ecouter", "pour", "dormir",
            "calme", "travail", "pause"
        }
    }

    # Standard BCP-47 Speech Recognition codes
    SPEECH_CODES = {
        "en": "en-IN",
        "hi": "hi-IN",
        "hinglish": "hi-IN",
        "kn": "kn-IN",
        "kannada-english": "kn-IN",
        "te": "te-IN",
        "telugu-english": "te-IN",
        "ta": "ta-IN",
        "tamil-english": "ta-IN",
        "ml": "ml-IN",
        "bn": "bn-IN",
        "es": "es-ES",
        "fr": "fr-FR"
    }

    # Display names
    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi",
        "hinglish": "Hinglish (Hindi-English)",
        "kn": "Kannada",
        "kannada-english": "Kannada-English",
        "te": "Telugu",
        "telugu-english": "Telugu-English",
        "ta": "Tamil",
        "tamil-english": "Tamil-English",
        "ml": "Malayalam",
        "bn": "Bengali",
        "es": "Spanish",
        "fr": "French"
    }

    def detect_language(self, text: str) -> str:
        """
        Detects the primary language of the text.
        Returns language code (e.g., 'en', 'hi', 'kn', 'hinglish', etc.).
        """
        if not text or not text.strip():
            return "en"

        cleaned = text.strip()

        # 1. Check Native Scripts
        for lang, pattern in self.SCRIPT_RANGES.items():
            if pattern.search(cleaned):
                return lang

        # 2. Check Romanized / Code-switching Keywords
        words = set(re.findall(r"\b[a-zA-Z]+\b", cleaned.lower()))
        max_overlap = 0
        best_lang = "en"

        for lang, vocab in self.ROMAN_LEXICONS.items():
            overlap = len(words.intersection(vocab))
            if overlap > max_overlap:
                max_overlap = overlap
                best_lang = lang

        if max_overlap > 0:
            return best_lang

        # 3. Default to English
        return "en"

    def get_speech_recognition_code(self, lang_code: str) -> str:
        """Returns BCP-47 speech recognition language code."""
        return self.SPEECH_CODES.get(lang_code, "en-IN")

    def get_language_display_name(self, lang_code: str) -> str:
        """Returns human-readable name of the language."""
        return self.LANGUAGE_NAMES.get(lang_code, "English")
