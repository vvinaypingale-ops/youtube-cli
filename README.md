# MUSIQ AI – Intelligent Multilingual Music Assistant
> An AI-powered, multilingual, conversational music assistant and CLI tool built on Python and YouTube Music.

---

MUSIQ AI is an intelligent, Python-based Command-Line Interface (CLI) application that brings conversational Artificial Intelligence to YouTube Music. It transforms traditional music discovery into an interactive experience by allowing users to search, discover, and interact with music using natural-language commands in multiple languages.

Instead of relying on manual searches or predefined commands, users can simply describe what they want to listen to. The AI assistant understands their intent, preferences, mood, and activities to provide relevant music suggestions and a personalized discovery experience.

---

## 🌟 Highlights & Key Features

- **100% Free**: No subscriptions, developer account approvals, or paid API keys required.
- **Multilingual Understanding**: Seamlessly understands commands in **English, Hindi, Kannada, Telugu, Tamil, Malayalam, Bengali, Spanish, French, and Hinglish**.
- **Context & Mood Intelligence**: Interprets user activities (*coding*, *workout*, *study*, *travel*, *sleep*) and emotional contexts (*relaxing*, *energetic*, *peaceful*, *sad*, *happy*).
- **Time-Targeted AI Playlist Generator**: Creates custom playlists matching exact durations (e.g., *"Create a 45-minute Hindi playlist for a relaxing evening"*).
- **Persistent User Memory**: Remembers preferred language, favorite artists, liked/disliked songs, and activity preferences via local SQLite storage.
- **Multilingual Voice Assistant**: Hands-free voice recognition with native Windows microphone capture via `sounddevice` and Google Speech.
- **Full CLI & Retro Dashboard**: Includes standard CLI subcommands, an auto-completing interactive shell, and a full-screen Terminal UI (TUI).

---

## 🏛️ System Architecture

```text
├── ai_engine/               # Multilingual NLU, Pydantic Intent Schema, LLM & Rule Parser
├── youtube_music/           # YouTube Music Integration (Search, Playback, Playlist, Auth)
├── music_engine/            # Mood Classifier, Track Ranker, Discovery & Playlist Generator
├── memory/                  # SQLite Persistence (User Preferences, Feedback, Playlists)
├── voice/                   # Microphone Input, Windows SAPI TTS & Voice Assistant Loop
├── tests/                   # 30+ Automated Unit Tests (100% offline & mocked)
├── main.py                  # Primary CLI & Conversational AI Entry Point
├── shell.py                 # Interactive Auto-Completing Shell
├── tui.py                   # Terminal UI Visual Dashboard
└── voiceActions.py          # Standalone Voice Assistant Entry Point
```

---

## 📦 Installation & Setup

### 1. Install Dependencies
```shell
pip install -r requirements.txt
```

### 2. Environment Configuration (`.env`)
The project runs out-of-the-box in public mode without any API keys. If you wish to use an LLM for intent parsing, configure your optional key in `.env`:
```env
# Optional LLM Keys (Falls back to high-accuracy offline multilingual parser if omitted)
GEMINI_API_KEY=your_gemini_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🎧 Usage Guide

### 1. Interactive Conversational AI Assistant
Launch the multilingual AI assistant:
```shell
python main.py ai
```
**Example Multilingual Conversations:**
- 🇮🇳 **Hindi**: *"Mujhe Arijit Singh ke gaane sunne hain."*
- 🇮🇳 **Kannada**: *"Nanage workout ge energetic songs beku."*
- 🇮🇳 **Telugu**: *"Naaku peaceful music play cheyyi."*
- 🇮🇳 **Tamil**: *"Enakku coding panna instrumental music venum."*
- 🇮🇳 **Hinglish**: *"Bhai coding ke liye kuch instrumental music chalao."*
- 🇬🇧 **English**: *"Play something relaxing for studying."*
- 🇪🇸 **Spanish**: *"Reproducir musica relajante para dormir."*
- 🇫🇷 **French**: *"Jouer de la musique calme pour travailler."*
- ⏱️ **AI Playlist**: *"Create a 30-minute Hindi playlist for relaxing."*
- 🔍 **Similar Music**: *"Play music similar to Coldplay."*

### 2. Hands-Free Voice Assistant
Run the voice-controlled assistant:
```shell
python main.py voice
# or
python voiceActions.py
```
- Say: **`Hello`** to activate.
- Speak: **`Play Believer`**, **`Nanage energetic songs beku`**, or **`Pause`**.
- Say: **`Exit`** or press `Ctrl + C` to stop.

### 3. Direct CLI Commands
```shell
# Search and stream any song
python main.py play "Rolling in the Deep"

# Toggle pause / resume system-wide
python main.py pause
python main.py resume

# Artist statistics & channel
python main.py artist-info "Coldplay"

# Search curated playlists
python main.py get-playlists "Top Hits"

# View all commands
python main.py --help
```

### 4. Interactive Shell Mode
```shell
python shell.py
```

### 5. Terminal UI Visual Dashboard
```shell
python tui.py
```

---

## 🧪 Automated Testing
Run the complete 30-test automated test suite:
```shell
python -m unittest discover tests
```

---

## ⚖️ Supported Operations & Technical Limitations

| Operation | Implementation Details | Supported Mode |
|---|---|---|
| **Song & Video Search** | `ytmusicapi.search(filter="songs")` | Supported (Public & Authenticated) |
| **Artist Information** | `ytmusicapi.search(filter="artists")` & `get_artist` | Supported (Public & Authenticated) |
| **Playlist Browsing** | `ytmusicapi.search(filter="playlists")` & `get_playlist` | Supported (Public & Authenticated) |
| **Playback & Streaming** | System browser streaming (`music.youtube.com/watch?v=...`) + Windows media keys | Supported (No DRM tampering) |
| **Play / Pause Controls** | Global Windows Media Keys (`ctypes` keybd_event `0xB3`) | Supported across Windows |
| **Local Playlist Curation** | Saved in SQLite + playable YouTube multi-video queue URLs | Supported without logins |
| **Remote Account Playlists** | `ytmusicapi.create_playlist` | Requires user's `oauth.json` |

---

## 💡 Acknowledgements & Credits

This project builds upon and extends the foundational concepts of the original Spotify CLI project by [Alok Raj](https://github.com/alokraj-05). MUSIQ AI extends that foundation with native YouTube Music integration, offline-first SQLite memory, and AI-powered multilingual conversational capabilities.

- **Original Foundation:** [github.com/alokraj-05/spotify-cli](https://github.com/alokraj-05/spotify-cli)
- **Developed by:** V Vinay Pingale
