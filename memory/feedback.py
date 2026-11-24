import json
from memory.database import get_db_connection

class FeedbackManager:
    """Manages liked/disliked tracks and playlist history."""

    def record_like(self, track_title: str, artist_name: str = "", video_id: str = None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO track_feedback (track_title, artist_name, video_id, is_liked, created_at)
                VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(track_title, artist_name) DO UPDATE SET
                    is_liked = 1,
                    video_id = COALESCE(excluded.video_id, track_feedback.video_id),
                    created_at = CURRENT_TIMESTAMP
            """, (track_title.strip(), artist_name.strip(), video_id))

    def record_dislike(self, track_title: str, artist_name: str = "", video_id: str = None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO track_feedback (track_title, artist_name, video_id, is_liked, created_at)
                VALUES (?, ?, ?, 0, CURRENT_TIMESTAMP)
                ON CONFLICT(track_title, artist_name) DO UPDATE SET
                    is_liked = 0,
                    video_id = COALESCE(excluded.video_id, track_feedback.video_id),
                    created_at = CURRENT_TIMESTAMP
            """, (track_title.strip(), artist_name.strip(), video_id))

    def is_disliked(self, track_title: str, artist_name: str = "") -> bool:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT is_liked FROM track_feedback
                WHERE LOWER(track_title) = LOWER(?) AND (artist_name = '' OR LOWER(artist_name) = LOWER(?))
            """, (track_title.strip(), artist_name.strip()))
            row = cursor.fetchone()
            return row is not None and row["is_liked"] == 0

    def is_liked(self, track_title: str, artist_name: str = "") -> bool:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT is_liked FROM track_feedback
                WHERE LOWER(track_title) = LOWER(?) AND (artist_name = '' OR LOWER(artist_name) = LOWER(?))
            """, (track_title.strip(), artist_name.strip()))
            row = cursor.fetchone()
            return row is not None and row["is_liked"] == 1

    def get_liked_tracks(self) -> list:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT track_title, artist_name, video_id FROM track_feedback WHERE is_liked = 1 ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def record_playlist(self, name: str, description: str, duration_seconds: int, track_count: int, video_ids: list):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO playlist_history (playlist_name, description, duration_seconds, track_count, video_ids_json)
                VALUES (?, ?, ?, ?, ?)
            """, (name, description, duration_seconds, track_count, json.dumps(video_ids)))

    def get_playlist_history(self, limit: int = 10) -> list:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT playlist_name, description, duration_seconds, track_count, video_ids_json, created_at
                FROM playlist_history ORDER BY created_at DESC LIMIT ?
            """, (limit,))
            results = []
            for row in cursor.fetchall():
                d = dict(row)
                d["video_ids"] = json.loads(d["video_ids_json"]) if d["video_ids_json"] else []
                results.append(d)
            return results
