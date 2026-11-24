class ResponseGenerator:
    """
    Generates natural, context-aware multilingual responses
    for English, Hindi, Hinglish, Kannada, Telugu, Tamil, Spanish, French, etc.
    """

    RESPONSES = {
        "en": {
            "playing_track": "Playing '{title}' by {artist} on YouTube Music.",
            "playing_artist": "Playing top songs by {artist}.",
            "mood_recommendation": "Found tracks matching your {context}: playing '{title}' by {artist}.",
            "paused": "⏸️ Playback paused.",
            "resumed": "▶️ Playback resumed.",
            "next": "⏭️ Skipped to the next track.",
            "prev": "⏮️ Returned to the previous track.",
            "not_found": "I couldn't find tracks for '{query}'. Try another search!",
            "playlist_proposed": "Curated {count} songs ({duration}) for '{name}'. Shall I create and play it?",
            "playlist_created": "✅ Playlist '{name}' created with {count} tracks ({duration})! Starting stream.",
            "similar": "Found tracks stylistically similar to {target}: starting with '{title}' by {artist}."
        },
        "hi": {
            "playing_track": "यूट्यूब म्यूजिक पर {artist} का '{title}' गाना बजाया जा रहा है।",
            "playing_artist": "{artist} के बेहतरीन गाने आपके लिए चला रहा हूँ।",
            "mood_recommendation": "आपके {context} मूड के अनुसार: '{title}' ({artist}) प्रस्तुत है।",
            "paused": "⏸️ गाना रोक दिया गया है।",
            "resumed": "▶️ गाना फिर से शुरू हो गया है।",
            "next": "⏭️ अगला गाना बजाया जा रहा है।",
            "prev": "⏮️ पिछला गाना बजाया जा रहा है।",
            "not_found": "'{query}' के लिए गाने नहीं मिले। कृपया कुछ और खोजें!",
            "playlist_proposed": "'{name}' के लिए {count} गाने ({duration}) तैयार किए हैं। क्या मैं इसे चलाऊँ?",
            "playlist_created": "✅ '{name}' प्लेलिस्ट तैयार हो गई है! संगीत का आनंद लें।",
            "similar": "{target} से मिलते-जुलते गाने: '{title}' ({artist}) प्रस्तुत है।"
        },
        "hinglish": {
            "playing_track": "YouTube Music par '{title}' by {artist} play kar raha hoon.",
            "playing_artist": "{artist} ke superhit gaane play kar raha hoon.",
            "mood_recommendation": "Aapke {context} mood ke liye perfect gaana mila: '{title}' by {artist}!",
            "paused": "⏸️ Playback pause kar diya hai.",
            "resumed": "▶️ Playback resume ho gaya hai.",
            "next": "⏭️ Agla gaana laga diya hai.",
            "prev": "⏮️ Pichla gaana bajaya ja raha hai.",
            "not_found": "'{query}' ka koi track nahi mila, koi aur gaana try karein?",
            "playlist_proposed": "'{name}' ke liye {count} songs ({duration}) ready hain. Create karke play karein?",
            "playlist_created": "✅ '{name}' playlist ban gayi hai! Stream shuru ho rahi hai.",
            "similar": "{target} jaise gaane: '{title}' by {artist} play kar raha hoon."
        },
        "kn": {
            "playing_track": "ಯೂಟ್ಯೂಬ್ ಮ್ಯೂಸಿಕ್‌ನಲ್ಲಿ {artist} ಅವರ '{title}' ಗೀತೆಯನ್ನು ಪ್ಲೇ ಮಾಡುತ್ತಿದ್ದೇನೆ.",
            "playing_artist": "{artist} ಅವರ ಜನಪ್ರಿಯ ಹಾಡುಗಳನ್ನು ಪ್ಲೇ ಮಾಡುತ್ತಿದ್ದೇನೆ.",
            "mood_recommendation": "ನಿಮ್ಮ {context} ಮೂಡ್‌ಗೆ ತಕ್ಕಂತೆ: '{title}' ({artist}) ಗೀತೆ ಸಿದ್ಧವಾಗಿದೆ.",
            "paused": "⏸️ ಪ್ಲೇಬ್ಯಾಕ್ ನಿಲ್ಲಿಸಲಾಗಿದೆ.",
            "resumed": "▶️ ಪ್ಲೇಬ್ಯಾಕ್ ಮುಂದುವರಿದಿದೆ.",
            "next": "⏭️ ಮುಂದಿನ ಹಾಡಿಗೆ ಬದಲಾಯಿಸಲಾಗಿದೆ.",
            "prev": "⏮️ ಹಿಂದಿನ ಹಾಡಿಗೆ ಮರಳಲಾಗಿದೆ.",
            "not_found": "'{query}' ಗೆ ಯಾವುದೇ ಹಾಡುಗಳು ಸಿಗಲಿಲ್ಲ.",
            "playlist_proposed": "'{name}' ಗಾಗಿ {count} ಹಾಡುಗಳನ್ನು ({duration}) ಆಯ್ಕೆ ಮಾಡಲಾಗಿದೆ. ಪ್ಲೇಲಿಸ್ಟ್ ರಚಿಸಲೆ?",
            "playlist_created": "✅ '{name}' ಪ್ಲೇಲಿಸ್ಟ್ ಸಿದ್ಧವಾಗಿದೆ!",
            "similar": "{target} ಅವರಂತೆಯೇ ಇರುವ ಗೀತೆಗಳು: '{title}' ({artist})."
        },
        "kannada-english": {
            "playing_track": "YouTube Music nalli {artist} avara '{title}' play madthiddini.",
            "playing_artist": "{artist} avara top songs play madthiddini.",
            "mood_recommendation": "Nimma {context} ge suit aagova song: '{title}' by {artist}.",
            "paused": "⏸️ Playback pause aagide.",
            "resumed": "▶️ Playback resume aagide.",
            "next": "⏭️ Next song ge skip madthiddini.",
            "prev": "⏮️ Previous song ge hogthiddini.",
            "not_found": "'{query}' ge haadugalu sigalilla.",
            "playlist_proposed": "'{name}' ge {count} songs ({duration}) select madidini. Create madi play madla?",
            "playlist_created": "✅ '{name}' playlist create aagide! Enjoy madi.",
            "similar": "{target} thara song: '{title}' by {artist} play madthiddini."
        },
        "te": {
            "playing_track": "యూట్యూబ్ మ్యూజిక్‌లో {artist} పాడిన '{title}' ప్లే అవుతోంది.",
            "playing_artist": "{artist} యొక్క పాపులర్ పాటలను ప్లే చేస్తున్నాను.",
            "mood_recommendation": "మీ {context} కోసం: '{title}' ({artist}) పాటను ప్లే చేస్తున్నాను.",
            "paused": "⏸️ ప్లేబ్యాక్ ఆపివేయబడింది.",
            "resumed": "▶️ ప్లేబ్యాక్ కొనసాగుతోంది.",
            "next": "⏭️ తదుపరి పాటకు వెళ్తున్నాను.",
            "prev": "⏮️ మునుపటి పాటకు వెళ్తున్నాను.",
            "not_found": "'{query}' కోసం పాటలు లభించలేదు.",
            "playlist_proposed": "'{name}' కోసం {count} పాటలు సిద్ధం చేసాను. ప్లేలిస్ట్ సృష్టించాలా?",
            "playlist_created": "✅ '{name}' ప్లేలిస్ట్ పూర్తయింది!",
            "similar": "{target} లాంటి పాటలు: '{title}' ({artist})."
        },
        "telugu-english": {
            "playing_track": "YouTube Music lo '{title}' by {artist} play chesthunnanu.",
            "playing_artist": "{artist} top songs play chesthunnanu.",
            "mood_recommendation": "Mee {context} mood ki perfect song: '{title}' by {artist}!",
            "paused": "⏸️ Playback pause chesamu.",
            "resumed": "▶️ Playback resume ayindi.",
            "next": "⏭️ Next song ki skip chesthunnanu.",
            "prev": "⏮️ Previous song ki velthunnanu.",
            "not_found": "'{query}' ki paatalu dhorakaledhu.",
            "playlist_proposed": "'{name}' kosam {count} songs ready. Create chesi play cheyyala?",
            "playlist_created": "✅ '{name}' playlist create ayindi! Enjoy cheyyandi.",
            "similar": "{target} lanti paatalu: '{title}' by {artist} play chesthunnanu."
        },
        "ta": {
            "playing_track": "யூடியூப் மியூசிக்கில் {artist} பாடிய '{title}' பாடல் ஒலிக்கிறது.",
            "playing_artist": "{artist} அவர்களின் சிறந்த பாடல்களை இயக்குகிறேன்.",
            "mood_recommendation": "உங்கள் {context} மனநிலைக்கு ஏற்ற பாடல்: '{title}' ({artist}).",
            "paused": "⏸️ பாடல் நிறுத்தப்பட்டது.",
            "resumed": "▶️ பாடல் மீண்டும் ஒலிக்கிறது.",
            "next": "⏭️ அடுத்த பாடலுக்கு மாறுகிறது.",
            "prev": "⏮️ முந்தைய பாடலுக்கு மாறுகிறது.",
            "not_found": "'{query}' பாடல் எதுவும் கிடைக்கவில்லை.",
            "playlist_proposed": "'{name}' க்காக {count} பாடல்கள் தயாராக உள்ளன. ப்ளேலிஸ்ட் உருவாக்கலாமா?",
            "playlist_created": "✅ '{name}' ப்ளேலிஸ்ட் தயாராகிவிட்டது!",
            "similar": "{target} போன்ற பாடல்கள்: '{title}' ({artist})."
        },
        "tamil-english": {
            "playing_track": "YouTube Music la '{title}' by {artist} play panren.",
            "playing_artist": "{artist} oda top hits play panren.",
            "mood_recommendation": "Unga {context} mood ku best song: '{title}' by {artist}!",
            "paused": "⏸️ Playback pause panniten.",
            "resumed": "▶️ Playback resume aaiduchu.",
            "next": "⏭️ Adutha paattukku skip panren.",
            "prev": "⏮️ Munnaadi paatta play panren.",
            "not_found": "'{query}' ku paattu kidaikkala.",
            "playlist_proposed": "'{name}' ku {count} songs ready. Create panni play pannalaama?",
            "playlist_created": "✅ '{name}' playlist create aaiduchu! Enjoy pannunga.",
            "similar": "{target} madhiri songs: '{title}' by {artist} play panren."
        },
        "es": {
            "playing_track": "Reproduciendo '{title}' de {artist} en YouTube Music.",
            "playing_artist": "Reproduciendo los mejores exitos de {artist}.",
            "mood_recommendation": "Musica para tu momento {context}: '{title}' de {artist}.",
            "paused": "⏸️ Reproduccion pausada.",
            "resumed": "▶️ Reproduccion reanudada.",
            "next": "⏭️ Saltando a la siguiente cancion.",
            "prev": "⏮️ Volviendo a la cancion anterior.",
            "not_found": "No encontre pistas para '{query}'.",
            "playlist_proposed": "He preparado {count} canciones ({duration}) para '{name}'. ¿Deseas crearla?",
            "playlist_created": "✅ ¡Lista '{name}' creada con exito!",
            "similar": "Pistas similares a {target}: '{title}' de {artist}."
        },
        "fr": {
            "playing_track": "Lecture de '{title}' par {artist} sur YouTube Music.",
            "playing_artist": "Lecture des meilleurs titres de {artist}.",
            "mood_recommendation": "Musique pour votre moment {context} : '{title}' par {artist}.",
            "paused": "⏸️ Lecture en pause.",
            "resumed": "▶️ Lecture reprise.",
            "next": "⏭️ Piste suivante.",
            "prev": "⏮️ Piste precedente.",
            "not_found": "Aucun titre trouve pour '{query}'.",
            "playlist_proposed": "{count} titres prepares ({duration}) pour '{name}'. Voulez-vous la creer ?",
            "playlist_created": "✅ Playlist '{name}' creee avec succes !",
            "similar": "Titres similaires a {target} : '{title}' par {artist}."
        }
    }

    def format(self, lang: str, key: str, **kwargs) -> str:
        lang_key = lang.lower() if lang else "en"
        templates = self.RESPONSES.get(lang_key, self.RESPONSES["en"])
        template = templates.get(key, self.RESPONSES["en"].get(key, ""))
        try:
            return template.format(**kwargs)
        except Exception:
            return template
