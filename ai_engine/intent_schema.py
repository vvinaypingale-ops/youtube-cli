from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class IntentType(str, Enum):
    PLAY_TRACK = "PLAY_TRACK"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    NEXT_TRACK = "NEXT_TRACK"
    PREVIOUS_TRACK = "PREVIOUS_TRACK"
    SEARCH_TRACK = "SEARCH_TRACK"
    SEARCH_ARTIST = "SEARCH_ARTIST"
    PLAY_ARTIST = "PLAY_ARTIST"
    SEARCH_ALBUM = "SEARCH_ALBUM"
    SEARCH_PLAYLIST = "SEARCH_PLAYLIST"
    PLAY_PLAYLIST = "PLAY_PLAYLIST"
    CREATE_PLAYLIST = "CREATE_PLAYLIST"
    ADD_TO_PLAYLIST = "ADD_TO_PLAYLIST"
    DISCOVER_MUSIC = "DISCOVER_MUSIC"
    MOOD_RECOMMENDATION = "MOOD_RECOMMENDATION"
    SIMILAR_MUSIC = "SIMILAR_MUSIC"
    CURRENTLY_PLAYING = "CURRENTLY_PLAYING"
    USER_PREFERENCES = "USER_PREFERENCES"
    SET_LANGUAGE = "SET_LANGUAGE"
    CLARIFICATION = "CLARIFICATION"
    UNKNOWN = "UNKNOWN"

class MusicIntent(BaseModel):
    """Pydantic validated structured music intent representation."""
    intent: IntentType = Field(description="The primary action to perform")
    query: Optional[str] = Field(default=None, description="General search query or song title")
    artist: Optional[str] = Field(default=None, description="Identified artist name")
    song_title: Optional[str] = Field(default=None, description="Identified specific song title")
    album: Optional[str] = Field(default=None, description="Identified album title")
    genre: Optional[str] = Field(default=None, description="Music genre (e.g. classical, edm, lo-fi, acoustic)")
    mood: Optional[str] = Field(default=None, description="Mood category (e.g. relaxing, energetic, sad, happy, peaceful)")
    activity: Optional[str] = Field(default=None, description="Activity context (e.g. coding, workout, study, travel, sleep)")
    language: Optional[str] = Field(default=None, description="Target music language (e.g. Hindi, Kannada, Telugu, Tamil, English)")
    duration_minutes: Optional[int] = Field(default=None, description="Target playlist length in minutes")
    playlist_name: Optional[str] = Field(default=None, description="Name for the generated or target playlist")
    target_language: Optional[str] = Field(default=None, description="Target conversation language for SET_LANGUAGE")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")
    detected_language: str = Field(default="en", description="Detected language code of the user input")
    clarification_prompt: Optional[str] = Field(default=None, description="Clarification message if request is ambiguous")
    requires_confirmation: bool = Field(default=False, description="Whether action requires user confirmation")
    raw_input: str = Field(default="", description="Original user text")
