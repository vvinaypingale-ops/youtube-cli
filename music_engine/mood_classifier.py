class MoodClassifier:
    """
    Translates user communicated moods and activity contexts
    into musical attributes and search descriptors.
    """

    ACTIVITY_PROFILES = {
        "coding": {
            "genres": ["instrumental", "lo-fi", "synthwave", "ambient"],
            "mood": "focus",
            "search_query": "coding focus lo-fi instrumental",
            "explanation": "Focused instrumental and lo-fi tracks to maintain coding flow."
        },
        "workout": {
            "genres": ["edm", "hip-hop", "rock", "fast pop"],
            "mood": "energetic",
            "search_query": "energetic workout motivation gym hits",
            "explanation": "High-tempo energetic tracks designed to boost workout stamina."
        },
        "study": {
            "genres": ["classical", "piano", "ambient", "acoustic"],
            "mood": "calm",
            "search_query": "peaceful study instrumental concentration",
            "explanation": "Low-distraction peaceful instrumental music for deep focus."
        },
        "travel": {
            "genres": ["indie", "acoustic pop", "rock"],
            "mood": "upbeat",
            "search_query": "road trip travel driving songs",
            "explanation": "Vibrant and scenic tunes curated for journeys and road trips."
        },
        "sleep": {
            "genres": ["ambient", "soft piano", "nature sounds"],
            "mood": "peaceful",
            "search_query": "deep sleep peaceful relaxing ambient",
            "explanation": "Gentle, soothing melodies to promote peaceful sleep."
        }
    }

    MOOD_PROFILES = {
        "relaxing": {
            "genres": ["acoustic", "chillout", "lo-fi"],
            "search_query": "relaxing peaceful chill songs",
            "explanation": "Calm, comforting melodies to unwind and de-stress."
        },
        "peaceful": {
            "genres": ["classical", "acoustic", "flute", "piano"],
            "search_query": "peaceful serene soothing instrumental",
            "explanation": "Serene and peaceful melodies to bring tranquility."
        },
        "energetic": {
            "genres": ["edm", "dance", "electronic", "pop"],
            "search_query": "energetic upbeat dance party hits",
            "explanation": "Fast-paced, vibrant rhythms to elevate energy."
        },
        "sad": {
            "genres": ["soulful", "acoustic ballads", "melancholy"],
            "search_query": "comforting acoustic emotional soulful songs",
            "explanation": "Heartfelt and comforting songs for emotional reflection."
        },
        "happy": {
            "genres": ["feel-good pop", "upbeat", "indie pop"],
            "search_query": "cheerful joyful feel good happy hits",
            "explanation": "Uplifting and cheerful songs to brighten your day."
        },
        "focus": {
            "genres": ["lo-fi", "ambient", "electronic beats"],
            "search_query": "deep focus lo-fi study instrumental",
            "explanation": "Steady rhythms to support concentration and productivity."
        }
    }

    def get_query_and_explanation(self, mood: str = None, activity: str = None, language: str = None) -> tuple:
        """
        Returns (search_query, explanation) based on mood and activity.
        """
        query_parts = []
        explanations = []

        if language:
            query_parts.append(language)

        if activity and activity.lower() in self.ACTIVITY_PROFILES:
            prof = self.ACTIVITY_PROFILES[activity.lower()]
            query_parts.append(prof["search_query"])
            explanations.append(prof["explanation"])
        elif mood and mood.lower() in self.MOOD_PROFILES:
            prof = self.MOOD_PROFILES[mood.lower()]
            query_parts.append(prof["search_query"])
            explanations.append(prof["explanation"])
        else:
            query_parts.append(f"{mood or ''} {activity or ''} music".strip())
            explanations.append("Curated tracks matching your request.")

        full_query = " ".join([p for p in query_parts if p]).strip()
        explanation = " ".join(explanations)
        return full_query, explanation
