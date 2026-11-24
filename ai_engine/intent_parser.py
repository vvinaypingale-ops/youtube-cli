import os
import re
import json
from ai_engine.intent_schema import MusicIntent, IntentType
from ai_engine.language_detector import LanguageDetector
from ai_engine.prompts import SYSTEM_PROMPT, CLARIFICATION_PROMPTS

class IntentParser:
    """
    Intelligent Multilingual Semantic Intent Parser.
    Combines LLM intelligence (Gemini / OpenAI) when API keys are available
    with an advanced, multi-stage semantic & conversational rule engine.
    """

    # Conversational preambles to strip for clean entity resolution
    PREAMBLE_PATTERNS = [
        # English
        r"^(?:can you|could you|would you|please|i want to|i'd like to|i would like to|put on|play me|let's hear|let me hear|find me|give me|start|how about|search for)\s+(?:some\s+|a\s+|the\s+)?",
        # Hindi / Hinglish
        r"^(?:bhai|yaar|kripya|please)?\s*(?:mujhe|humein|mera)?\s*(?:kuch|thoda|koi|ek)?\s*(?:accha|badhiya|mast)?\s*(?:gaana|gaane|songs|music)?\s*(?:sunao|chalao|bajao|laga do|chala do|play karo)\s*",
        # Kannada / Kannada-English
        r"^(?:dayavittu|nanage|nange)?\s*(?:ondhu|kuch)?\s*(?:olle|hosa)?\s*(?:haadu|haadugalu|songs)?\s*(?:play maadi|haaku|kodi|kelabeku)\s*",
        # Telugu / Telugu-English
        r"^(?:dayachesi|naaku|naku)?\s*(?:manchi|kothha)?\s*(?:paata|paatalu|songs)?\s*(?:play cheyyi|veeyi|pettandi|vinali)\s*",
        # Tamil / Tamil-English
        r"^(?:dayavuseidhu|enakku)?\s*(?:nalla|pudhu)?\s*(?:paattu|paadalkal|songs)?\s*(?:podunga|play pannunga|kekkalam)\s*"
    ]

    def __init__(self):
        self.detector = LanguageDetector()
        self._init_llm_client()

    def _init_llm_client(self):
        self.llm_provider = None
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

        if self.gemini_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.gemini_key)
                self.llm_provider = "gemini"
            except Exception:
                pass
        elif self.openai_key:
            try:
                import openai
                openai.api_key = self.openai_key
                self.llm_provider = "openai"
            except Exception:
                pass

    def strip_preamble(self, text: str) -> str:
        """Strips conversational preambles and postpositions iteratively to uncover core subject."""
        cleaned = text.strip()
        prefix_pat = re.compile(
            r"^(can you|could you|would you|please|i want to|i'd like to|i would like to|put on|play me|play|let's hear|let me hear|find me|give me|start|how about|search for|stream|listen to|suno|chalao|bajao|kelu|podu|veeyi|bhai|yaar|kripya|mujhe|humein|mera|kuch|thoda|koi|ek|accha|badhiya|mast|dayavittu|nanage|nange|ondhu|olle|hosa|dayachesi|naaku|naku|manchi|kothha|dayavuseidhu|enakku|nalla|pudhu|some|a|the)\s+",
            flags=re.IGNORECASE
        )
        suffix_pat = re.compile(
            r"\s+(?:play maadi|play karo|play cheyyi|play pannunga|chalao|bajao|sunao|laga do|veeyi|podu|beku|chahiye|sunna hai)$",
            flags=re.IGNORECASE
        )

        prev = ""
        while prev != cleaned:
            prev = cleaned
            cleaned = prefix_pat.sub("", cleaned).strip()

        cleaned = suffix_pat.sub("", cleaned).strip()
        return cleaned

    def parse(self, text: str, context: dict = None) -> MusicIntent:
        raw_text = text.strip() if text else ""
        if not raw_text:
            return MusicIntent(
                intent=IntentType.UNKNOWN,
                raw_input="",
                clarification_prompt=CLARIFICATION_PROMPTS["en"]
            )

        detected_lang = self.detector.detect_language(raw_text)

        # 1. Try LLM if configured
        if self.llm_provider:
            intent = self._parse_with_llm(raw_text, detected_lang, context)
            if intent:
                return intent

        # 2. Advanced Multi-Stage Semantic Parser
        return self._parse_with_advanced_semantics(raw_text, detected_lang, context)

    def _parse_with_llm(self, text: str, detected_lang: str, context: dict) -> MusicIntent:
        try:
            prompt = f"{SYSTEM_PROMPT}\n\nContext: {json.dumps(context or {})}\nInput: {text}\nOutput JSON:"
            if self.llm_provider == "gemini":
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                raw_json = re.search(r"\{.*\}", response.text, re.DOTALL)
                if raw_json:
                    data = json.loads(raw_json.group(0))
                    data["raw_input"] = text
                    data["detected_language"] = detected_lang
                    return MusicIntent(**data)
        except Exception:
            pass
        return None

    def _parse_with_advanced_semantics(self, text: str, detected_lang: str, context: dict = None) -> MusicIntent:
        low = text.lower()
        context = context or {}

        # 1. Playback Controls
        if any(w in low for w in ["pause", "ruk jao", "roko", "nillisu", "aagu", "pausa", "stop"]):
            return MusicIntent(intent=IntentType.PAUSE, raw_input=text, detected_language=detected_lang)

        if any(w in low for w in ["resume", "chalu karo", "punararambha", "reproducir", "continue", "play again"]):
            return MusicIntent(intent=IntentType.RESUME, raw_input=text, detected_language=detected_lang)

        if any(w in low for w in ["next", "skip", "agla", "mundina", "next song", "siguiente", "maro paata"]):
            return MusicIntent(intent=IntentType.NEXT_TRACK, raw_input=text, detected_language=detected_lang)

        if any(w in low for w in ["previous", "pichla", "hinde", "prev song", "anterior", "venuka"]):
            return MusicIntent(intent=IntentType.PREVIOUS_TRACK, raw_input=text, detected_language=detected_lang)

        if any(w in low for w in ["what am i listening", "what is playing", "currently playing", "current song", "kaunsa gaana chal raha", "yava haadu"]):
            return MusicIntent(intent=IntentType.CURRENTLY_PLAYING, raw_input=text, detected_language=detected_lang)

        # 2. Extract Duration (e.g. 45-minute, 30 mins, 2 hours, half hour, 1 ghanta)
        duration_minutes = None
        if "half hour" in low or "half an hour" in low or "aadha ghanta" in low:
            duration_minutes = 30
        else:
            dur_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:-| )?\s*(minute|min|m|hour|hr|ghanta|ghante|hours)", low)
            if dur_match:
                val = float(dur_match.group(1))
                unit = dur_match.group(2)
                duration_minutes = int(val * 60) if ("hour" in unit or "hr" in unit or "ghant" in unit) else int(val)

        # 3. Target Language
        language = None
        for lang_name in ["Hindi", "Kannada", "Telugu", "Tamil", "Malayalam", "Bengali", "English", "Punjabi", "Spanish", "French", "Marathi", "Gujarati"]:
            if lang_name.lower() in low:
                language = lang_name
                break

        # 4. Activity Context
        activity = None
        if any(w in low for w in ["coding", "code", "programming", "develop", "developer", "hackathon"]):
            activity = "coding"
        elif any(w in low for w in ["workout", "gym", "exercise", "kasarattu", "running", "lifting", "cardio", "fitness"]):
            activity = "workout"
        elif any(w in low for w in ["study", "studying", "padhai", "odhalu", "chadavadam", "exam", "revision", "concentrat"]):
            activity = "study"
        elif any(w in low for w in ["travel", "travelling", "road trip", "journey", "drive", "driving", "safari"]):
            activity = "travel"
        elif any(w in low for w in ["sleep", "sleeping", "sona", "nidde", "thookam", "padukodaniki", "bedtime", "insomnia"]):
            activity = "sleep"

        # 5. Mood Context
        mood = None
        if any(w in low for w in ["peaceful", "shant", "sukoon", "serene", "prashanta"]):
            mood = "peaceful"
        elif any(w in low for w in ["relaxing", "relax", "calm", "chill", "unwind", "soothing", "stress"]):
            mood = "relaxing"
        elif any(w in low for w in ["energetic", "energy", "josh", "utsaha", "fast", "pumped", "party", "dance"]):
            mood = "energetic"
        elif any(w in low for w in ["sad", "heartbreak", "dard", "dukha", "emotional", "crying", "depressed", "low"]):
            mood = "sad"
        elif any(w in low for w in ["happy", "cheerful", "khushi", "santosa", "joyful", "upbeat", "celebrat"]):
            mood = "happy"
        elif any(w in low for w in ["focus", "deep focus", "ambient", "flow state"]):
            mood = "focus"
        elif any(w in low for w in ["romantic", "love", "pyar", "preethi", "prem"]):
            mood = "romantic"

        # 6. Genre
        genre = None
        if "instrumental" in low:
            genre = "instrumental"
        elif "lo-fi" in low or "lofi" in low:
            genre = "lo-fi"
        elif "classical" in low or "shastriya" in low or "carnatic" in low:
            genre = "classical"
        elif "acoustic" in low or "unplugged" in low:
            genre = "acoustic"
        elif "edm" in low or "electronic" in low or "techno" in low:
            genre = "edm"
        elif "rock" in low:
            genre = "rock"
        elif "pop" in low:
            genre = "pop"
        elif "hip hop" in low or "rap" in low:
            genre = "hip-hop"

        # 7. Playlist Intent
        if "playlist" in low and any(w in low for w in ["create", "make", "banao", "maadi", "new", "generate", "build", "curate", "tayyar"]):
            name_match = re.search(r"(?:called|named|name)\s+['\"]?([^'\"\n]+)['\"]?", text, re.IGNORECASE)
            pl_name = name_match.group(1).strip() if name_match else None
            if not pl_name:
                parts = [p for p in [language, mood, activity, genre] if p]
                pl_name = f"{' '.join(parts).title()} Mix" if parts else "Custom AI Playlist"

            return MusicIntent(
                intent=IntentType.CREATE_PLAYLIST,
                playlist_name=pl_name,
                duration_minutes=duration_minutes or 30,
                mood=mood,
                activity=activity,
                language=language,
                genre=genre,
                requires_confirmation=True,
                raw_input=text,
                detected_language=detected_lang
            )

        # 8. Similar Music Intent
        if any(w in low for w in ["similar to", "jaise gaane", "taraha", "resembling", "sounds like"]):
            sim_match = re.search(r"(?:similar to|jaise|sounds like)\s+([a-zA-Z\s]+)", text, re.IGNORECASE)
            target = sim_match.group(1).strip() if sim_match else ""
            target = self.strip_preamble(target)
            return MusicIntent(
                intent=IntentType.SIMILAR_MUSIC,
                artist=target,
                query=target,
                language=language,
                raw_input=text,
                detected_language=detected_lang
            )

        # 9. Artist Intent (Preposition & Postposition recognition)
        # Check famous artist names directly
        known_artists = [
            "Arijit Singh", "Atif Aslam", "Shreya Ghoshal", "Vijay Prakash", "Sid Sriram",
            "Sonu Nigam", "Taylor Swift", "Coldplay", "Ed Sheeran", "The Weeknd", "Eminem",
            "Imagine Dragons", "Anirudh", "A.R. Rahman", "AR Rahman", "Diljit Dosanjh",
            "K.J. Yesudas", "SPB", "S.P. Balasubrahmanyam", "Lata Mangeshkar", "Kishore Kumar",
            "Armaan Malik", "Neha Kakkar", "Jubin Nautiyal", "Prateek Kuhad", "Badshah", "Kanye West"
        ]
        for ka in known_artists:
            if ka.lower() in low:
                return MusicIntent(
                    intent=IntentType.PLAY_ARTIST,
                    artist=ka,
                    query=ka,
                    mood=mood,
                    genre=genre,
                    language=language,
                    raw_input=text,
                    detected_language=detected_lang
                )

        # Indian post-position patterns (e.g. "Mohit Chauhan ke gaane", "Sanjith Hegde haadugalu")
        post_match = re.search(r"(?:mujhe|nanage|naaku|enakku)?\s*([a-zA-Z\s]+?)\s+(?:ke\s+gaane|ke\s+songs|haadugalu|paatalu|paadalkal)", text, re.IGNORECASE)
        if post_match:
            art = post_match.group(1).strip()
            if art and art.lower() not in ["kuch", "thoda", "mast", "some"]:
                return MusicIntent(
                    intent=IntentType.PLAY_ARTIST,
                    artist=art,
                    query=art,
                    mood=mood,
                    language=language,
                    raw_input=text,
                    detected_language=detected_lang
                )

        # English preposition pattern (e.g. "by Arijit Singh", "singer Shreya Ghoshal")
        artist_match = re.search(r"(?:by|singer|artist|tracks from)\s+([a-zA-Z\s]+)", text, re.IGNORECASE)
        if artist_match:
            art = artist_match.group(1).strip()
            art = re.sub(r"\s+(please|now|fast|today)$", "", art, flags=re.IGNORECASE)
            return MusicIntent(
                intent=IntentType.PLAY_ARTIST,
                artist=art,
                query=art,
                mood=mood,
                language=language,
                raw_input=text,
                detected_language=detected_lang
            )

        # 10. Mood / Activity / Context-driven recommendation
        if mood or activity or (language and any(w in low for w in ["music", "songs", "gaane", "haadugalu", "paatalu", "geet"])):
            desc_query = f"{language or ''} {mood or ''} {genre or ''} {activity or ''}".strip()
            return MusicIntent(
                intent=IntentType.MOOD_RECOMMENDATION,
                mood=mood,
                activity=activity,
                language=language,
                genre=genre,
                query=desc_query,
                raw_input=text,
                detected_language=detected_lang
            )

        # 11. Play Track (Cleaned search query)
        cleaned = self.strip_preamble(text)
        cleaned = re.sub(r"^(play|stream|listen to|suno|chalao|bajao|kelu|podu|veeyi)\s+", "", cleaned, flags=re.IGNORECASE).strip()

        if cleaned:
            return MusicIntent(
                intent=IntentType.PLAY_TRACK,
                query=cleaned,
                song_title=cleaned,
                language=language,
                raw_input=text,
                detected_language=detected_lang
            )

        return MusicIntent(
            intent=IntentType.UNKNOWN,
            raw_input=text,
            detected_language=detected_lang,
            clarification_prompt=CLARIFICATION_PROMPTS.get(detected_lang, CLARIFICATION_PROMPTS["en"])
        )
