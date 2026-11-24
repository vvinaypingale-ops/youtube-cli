import json
from memory.database import get_db_connection

class UserPreferencesManager:
    """Manages persistent user preferences in SQLite."""

    def __init__(self):
        pass

    def get_preference(self, key: str, default=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pref_value FROM user_preferences WHERE pref_key = ?", (key,))
            row = cursor.fetchone()
            if row:
                try:
                    return json.loads(row["pref_value"])
                except Exception:
                    return row["pref_value"]
            return default

    def set_preference(self, key: str, value):
        val_str = json.dumps(value) if not isinstance(value, str) else value
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_preferences (pref_key, pref_value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(pref_key) DO UPDATE SET
                    pref_value = excluded.pref_value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, val_str))

    def get_preferred_language(self, default="en") -> str:
        return self.get_preference("preferred_language", default)

    def set_preferred_language(self, language: str):
        self.set_preference("preferred_language", language.lower())

    def get_favorite_artists(self) -> list:
        return self.get_preference("favorite_artists", [])

    def add_favorite_artist(self, artist_name: str):
        artists = set(self.get_favorite_artists())
        artists.add(artist_name.strip())
        self.set_preference("favorite_artists", sorted(list(artists)))

    def remove_favorite_artist(self, artist_name: str):
        artists = set(self.get_favorite_artists())
        artists.discard(artist_name.strip())
        self.set_preference("favorite_artists", sorted(list(artists)))

    def get_favorite_genres(self) -> list:
        return self.get_preference("favorite_genres", [])

    def add_favorite_genre(self, genre: str):
        genres = set(self.get_favorite_genres())
        genres.add(genre.strip().lower())
        self.set_preference("favorite_genres", sorted(list(genres)))

    def set_activity_preference(self, activity: str, genre: str = None, mood: str = None, language: str = None):
        """Sets persistent preference for an activity (e.g. coding -> instrumental, workout -> energetic)."""
        act_key = activity.strip().lower()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activity_preferences (activity, genre, mood, language, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(activity) DO UPDATE SET
                    genre = COALESCE(excluded.genre, activity_preferences.genre),
                    mood = COALESCE(excluded.mood, activity_preferences.mood),
                    language = COALESCE(excluded.language, activity_preferences.language),
                    updated_at = CURRENT_TIMESTAMP
            """, (act_key, genre, mood, language))

    def get_activity_preference(self, activity: str) -> dict:
        act_key = activity.strip().lower()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT genre, mood, language FROM activity_preferences WHERE activity = ?", (act_key,))
            row = cursor.fetchone()
            if row:
                return {
                    "activity": act_key,
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "language": row["language"]
                }
            return {}

    def get_all_preferences(self) -> dict:
        result = {
            "preferred_language": self.get_preferred_language(),
            "favorite_artists": self.get_favorite_artists(),
            "favorite_genres": self.get_favorite_genres(),
            "activities": {}
        }
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT activity, genre, mood, language FROM activity_preferences")
            for row in cursor.fetchall():
                result["activities"][row["activity"]] = {
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "language": row["language"]
                }
        return result

    def delete_all_preferences(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_preferences")
            cursor.execute("DELETE FROM activity_preferences")
