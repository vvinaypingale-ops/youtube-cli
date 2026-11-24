import re
from filter.fuzzySearch import _normalize
from memory.user_preferences import UserPreferencesManager
from memory.feedback import FeedbackManager

class TrackRanker:
    """
    Preference-based multi-factor scoring and diversity ranking.
    """

    def __init__(self, prefs=None, feedback=None):
        self.prefs = prefs or UserPreferencesManager()
        self.feedback = feedback or FeedbackManager()

    def clean_title(self, title: str) -> str:
        """Removes noise like (Official Video), [4K], etc."""
        cleaned = re.sub(r"[\(\[\{].*?(official|video|audio|lyrics|hd|4k|remaster|visualizer).*?[\)\]\}]", "", title, flags=re.IGNORECASE)
        return _normalize(cleaned)

    def score_track(self, track: dict, target_artist: str = None, target_lang: str = None) -> float:
        """Calculates personalized relevance score (0-100+)."""
        title = track.get("title") or track.get("name", "")
        artist = track.get("artist", "")

        # Immediate filter if user explicitly disliked this track
        if self.feedback.is_disliked(title, artist):
            return -100.0

        score = 50.0

        # Favorite Artist bonus
        fav_artists = [a.lower() for a in self.prefs.get_favorite_artists()]
        if artist.lower() in fav_artists:
            score += 25.0

        # Target Artist bonus
        if target_artist and target_artist.lower() in artist.lower():
            score += 30.0

        # User Explicit Like bonus
        if self.feedback.is_liked(title, artist):
            score += 30.0

        # Preferred Language bonus
        pref_lang = self.prefs.get_preferred_language()
        if target_lang and pref_lang and target_lang.lower() == pref_lang.lower():
            score += 15.0

        return score

    def rank_and_deduplicate(self, tracks: list, max_per_artist: int = 2, target_artist: str = None) -> list:
        """
        Deduplicates tracks and sorts by score while ensuring artist diversity.
        """
        seen_titles = set()
        seen_ids = set()
        artist_counts = {}
        ranked = []

        # Calculate scores
        for t in tracks:
            v_id = t.get("video_id") or t.get("videoId")
            if v_id in seen_ids:
                continue

            cleaned_t = self.clean_title(t.get("title", ""))
            art_name = t.get("artist", "").strip()
            dedup_key = f"{cleaned_t}_{art_name.lower()}"
            if dedup_key in seen_titles:
                continue

            score = self.score_track(t, target_artist=target_artist)
            if score < 0:
                continue  # Disliked track

            item = dict(t)
            item["score"] = score
            ranked.append(item)
            seen_ids.add(v_id)
            seen_titles.add(dedup_key)

        # Sort descending by score
        ranked.sort(key=lambda x: x["score"], reverse=True)

        # Enforce artist diversity unless target_artist was specifically requested
        if target_artist:
            return ranked

        diverse_list = []
        overflow_list = []

        for item in ranked:
            art = item.get("artist", "Unknown").lower()
            count = artist_counts.get(art, 0)
            if count < max_per_artist:
                diverse_list.append(item)
                artist_counts[art] = count + 1
            else:
                overflow_list.append(item)

        # Append remaining tracks at the end
        return diverse_list + overflow_list
