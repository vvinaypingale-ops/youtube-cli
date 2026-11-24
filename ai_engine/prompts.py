SYSTEM_PROMPT = """You are MUSIQ AI, an intelligent multilingual music assistant.
Your task is to analyze natural language user commands in any language (English, Hindi, Kannada, Telugu, Tamil, Malayalam, Bengali, Spanish, French, Hinglish, etc.) and extract structured music intents.

CRITICAL INSTRUCTIONS:
1. Identify the primary intent from the allowed list:
   PLAY_TRACK, PAUSE, RESUME, NEXT_TRACK, PREVIOUS_TRACK, SEARCH_TRACK, SEARCH_ARTIST,
   SEARCH_ALBUM, SEARCH_PLAYLIST, CREATE_PLAYLIST, ADD_TO_PLAYLIST, DISCOVER_MUSIC,
   MOOD_RECOMMENDATION, SIMILAR_MUSIC, CURRENTLY_PLAYING, USER_PREFERENCES, SET_LANGUAGE, CLARIFICATION.
2. NEVER translate or alter song titles or artist names (e.g. keep "Arijit Singh", "Believer", "Kesariya", "Raataan Lambiyan" exactly as they are).
3. Extract entities: artist, song_title, genre, mood, activity, language, duration_minutes, playlist_name.
4. Output MUST be valid JSON conforming to the MusicIntent schema.
"""

MULTILINGUAL_FEW_SHOTS = [
    {
        "input": "Mujhe Arijit Singh ke gaane sunne hain.",
        "output": {
            "intent": "PLAY_ARTIST",
            "artist": "Arijit Singh",
            "language": "Hindi",
            "detected_language": "hinglish"
        }
    },
    {
        "input": "Nanage workout ge energetic songs beku.",
        "output": {
            "intent": "MOOD_RECOMMENDATION",
            "activity": "workout",
            "mood": "energetic",
            "language": "Kannada",
            "detected_language": "kannada-english"
        }
    },
    {
        "input": "Naaku peaceful music play cheyyi.",
        "output": {
            "intent": "MOOD_RECOMMENDATION",
            "mood": "peaceful",
            "language": "Telugu",
            "detected_language": "telugu-english"
        }
    },
    {
        "input": "Bhai coding ke liye kuch instrumental music chalao.",
        "output": {
            "intent": "MOOD_RECOMMENDATION",
            "activity": "coding",
            "genre": "instrumental",
            "mood": "focus",
            "detected_language": "hinglish"
        }
    },
    {
        "input": "Create a 45-minute Hindi playlist for a relaxing evening.",
        "output": {
            "intent": "CREATE_PLAYLIST",
            "duration_minutes": 45,
            "language": "Hindi",
            "mood": "relaxing",
            "playlist_name": "Relaxing Evening Hindi",
            "requires_confirmation": True
        }
    },
    {
        "input": "I am stressed. Suggest something peaceful.",
        "output": {
            "intent": "MOOD_RECOMMENDATION",
            "mood": "peaceful",
            "detected_language": "en"
        }
    },
    {
        "input": "Pause the music",
        "output": {
            "intent": "PAUSE",
            "detected_language": "en"
        }
    },
    {
        "input": "Next song please",
        "output": {
            "intent": "NEXT_TRACK",
            "detected_language": "en"
        }
    }
]

CLARIFICATION_PROMPTS = {
    "en": "Could you please specify which artist, song, or mood you would like to listen to?",
    "hi": "क्या आप बता सकते हैं कि आप कौन सा गाना, कलाकार या मूड सुनना चाहेंगे?",
    "hinglish": "Bhai kaunsa song ya artist sunna hai, thoda specify karoge?",
    "kn": "ಯಾವ ಹಾಡು ಅಥವಾ ಗಾಯಕರ ಗೀತೆಗಳನ್ನು ಕೇಳಲು ಇಷ್ಟಪಡುತ್ತೀರಿ ಎಂದು ತಿಳಿಸಿ?",
    "kannada-english": "Yava song athava artist beku antha heli?",
    "te": "మీరు ఏ పాట లేదా ఆర్టిస్ట్ వినాలనుకుంటున్నారో దయచేసి చెప్పండి?",
    "ta": "எந்த பாடல் அல்லது பாடகரின் பாடலை கேட்க விரும்புகிறீர்கள்?",
    "es": "¿Podrías especificar qué canción o artista te gustaría escuchar?",
    "fr": "Pourriez-vous préciser quelle chanson ou quel artiste vous aimeriez écouter ?"
}
