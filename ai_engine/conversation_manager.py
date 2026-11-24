import time
from ai_engine.intent_schema import MusicIntent, IntentType
from memory.user_preferences import UserPreferencesManager

class ConversationManager:
    """
    Manages multi-turn conversational context, pending slots, and confirmations.
    """

    def __init__(self, timeout_seconds: int = 300):
        self.timeout_seconds = timeout_seconds
        self.history = []
        self.pending_intent = None
        self.pending_confirmation = None
        self.last_activity = time.time()
        self.prefs = UserPreferencesManager()

    def is_expired(self) -> bool:
        return (time.time() - self.last_activity) > self.timeout_seconds

    def reset_if_expired(self):
        if self.is_expired():
            self.pending_intent = None
            self.pending_confirmation = None
            self.history = []
        self.last_activity = time.time()

    def add_turn(self, user_text: str, assistant_reply: str, intent: MusicIntent = None):
        self.reset_if_expired()
        self.history.append({
            "user": user_text,
            "assistant": assistant_reply,
            "intent": intent.model_dump() if intent else None,
            "timestamp": time.time()
        })
        # Keep last 10 turns
        if len(self.history) > 10:
            self.history.pop(0)

    def set_pending_confirmation(self, action: str, data: dict, prompt: str):
        self.pending_confirmation = {
            "action": action,
            "data": data,
            "prompt": prompt,
            "timestamp": time.time()
        }

    def clear_pending(self):
        self.pending_intent = None
        self.pending_confirmation = None

    def handle_followup_or_merge(self, raw_text: str, new_intent: MusicIntent) -> MusicIntent:
        """
        Merges follow-up responses into pending intent if an active slot is awaiting.
        """
        self.reset_if_expired()
        low = raw_text.strip().lower()

        # Check for confirmation to a pending action
        if self.pending_confirmation:
            if any(w in low for w in ["yes", "haan", "ha", "sari", "hou", "sure", "create", "kar do", "banao", "y", "ok", "proceed"]):
                action = self.pending_confirmation["action"]
                data = dict(self.pending_confirmation["data"])
                plan_object = self.pending_confirmation.get("plan_object")
                self.pending_confirmation = None
                return MusicIntent(
                    intent=IntentType(action),
                    raw_input=raw_text,
                    requires_confirmation=False,
                    **data
                )
            elif any(w in low for w in ["no", "nahi", "beda", "voddhu", "cancel", "stop", "rehne do"]):
                self.pending_confirmation = None
                return MusicIntent(
                    intent=IntentType.UNKNOWN,
                    raw_input=raw_text,
                    clarification_prompt="Action cancelled. What would you like to listen to instead?"
                )

        # Check if the user is answering a clarification (e.g. language or mood slot)
        if self.pending_intent:
            # If the user just specified a language (e.g., "Hindi", "Kannada")
            for lang in ["Hindi", "Kannada", "Telugu", "Tamil", "Malayalam", "Bengali", "English", "Punjabi"]:
                if lang.lower() in low:
                    merged = self.pending_intent.model_copy()
                    merged.language = lang
                    merged.raw_input = f"{self.pending_intent.raw_input} {raw_text}"
                    self.pending_intent = None
                    return merged

        # Check user activity memory if current intent has an activity without genre/mood
        if new_intent.activity and not new_intent.genre:
            stored_act = self.prefs.get_activity_preference(new_intent.activity)
            if stored_act and stored_act.get("genre"):
                new_intent.genre = stored_act["genre"]
            if stored_act and stored_act.get("mood") and not new_intent.mood:
                new_intent.mood = stored_act["mood"]

        # Default language fallback from user memory if not specified
        if not new_intent.language:
            pref_lang = self.prefs.get_preferred_language()
            if pref_lang and pref_lang != "en":
                new_intent.language = pref_lang.capitalize()

        return new_intent
