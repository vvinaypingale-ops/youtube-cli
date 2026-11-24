import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render running headers and footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        page_width, page_height = letter

        # Don't draw header on first page (cover/title)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(54, page_height - 36, "MUSIQ AI")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(100, page_height - 36, "• Intelligent Multilingual Music Assistant – Master Project Documentation")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, page_height - 42, page_width - 54, page_height - 42)

        # Footer on all pages
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 34, "Confidential & Proprietary • Engineering Project Documentation • Version 2.0")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_width - 54, 34, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, page_width - 54, 46)

        self.restoreState()


def build_pdf(filename="MUSIQ_AI_Project_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom palette
    PRIMARY = colors.HexColor("#1E3A8A")    # Deep Navy
    SECONDARY = colors.HexColor("#0284C7")  # Cyan / Blue
    TEXT_DARK = colors.HexColor("#0F172A")  # Slate 900
    TEXT_MUTED = colors.HexColor("#475569") # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Slate 50
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=SECONDARY,
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        textColor=TEXT_MUTED
    )

    h1_style = ParagraphStyle(
        "Header1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Header2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=PRIMARY
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12.5,
        textColor=PRIMARY
    )

    story = []

    # =========================================================================
    # COVER / TITLE BLOCK
    # =========================================================================
    story.append(Paragraph("MUSIQ AI – Intelligent Multilingual Music Assistant", title_style))
    story.append(Paragraph("Comprehensive Architectural Design, Technical Flow, and Engineering Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=SECONDARY, spaceAfter=10))

    meta_text = """
    <b>Project Title:</b> MUSIQ AI (formerly Spotify CLI) &nbsp;&nbsp;|&nbsp;&nbsp; <b>Version:</b> 2.0 Production Release<br/>
    <b>Architecture:</b> Multilingual AI NLU + YouTube Music Engine + SQLite Persistence + SAPI Voice Pipeline<br/>
    <b>Target Platforms:</b> Windows (Powershell/CMD), Linux, macOS &nbsp;&nbsp;|&nbsp;&nbsp; <b>Languages:</b> Python 3.10 - 3.14<br/>
    <b>Test Suite Status:</b> 33 / 33 Unit Tests Passing (100% Mocked Offline Execution in 0.358s)
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    p1 = """
    Modern music consumers, software developers, and students increasingly prefer command-line interfaces (CLI)
    and terminal dashboards over resource-heavy web and desktop GUI clients. However, conventional terminal music players
    suffer from severe technical bottlenecks:
    """
    story.append(Paragraph(p1, body_style))

    story.append(Paragraph("• <b>Strict Paywalls and Developer API Deprecations:</b> Major platforms like Spotify have restricted Web API access to active Premium subscribers, deprecated audio-feature recommendation endpoints, and capped Development Mode apps to 5 allowlisted users.", bullet_style))
    story.append(Paragraph("• <b>Rigid Keyword Interfaces:</b> Legacy tools demand strict, brittle commands (e.g. <code>play &lt;exact-track-name&gt;</code>) and crash when users speak or write in natural conversational phrasing.", bullet_style))
    story.append(Paragraph("• <b>Absence of Regional & Multilingual Intelligence:</b> Mainstream music assistants primarily parse English, failing to recognize Indian regional languages (Hindi, Kannada, Telugu, Tamil, Malayalam, Bengali) or romanized code-switching like Hinglish and Kannada-English.", bullet_style))

    p2 = """
    <b>The Solution:</b> This project transforms an existing Spotify CLI codebase into <b>MUSIQ AI</b>,
    an intelligent, zero-cost, multilingual music assistant powered by YouTube Music, custom Pydantic-validated
    semantic intent parsing, intelligent content discovery, time-targeted playlist generation, persistent SQLite memory,
    and hands-free voice control.
    """
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: HOW IT BENEFITS EVERYONE (STAKEHOLDER VALUE)
    # =========================================================================
    story.append(Paragraph("2. Real-World Benefits & Stakeholder Value Proposition", h1_style))
    p_ben = """
    MUSIQ AI was architected to democratize AI-driven music curation, providing concrete value across multiple
    user segments:
    """
    story.append(Paragraph(p_ben, body_style))

    benefits_data = [
        [
            Paragraph("User Segment", table_header),
            Paragraph("Primary Need / Problem", table_header),
            Paragraph("How MUSIQ AI Directly Solves It (Tangible Benefit)", table_header)
        ],
        [
            Paragraph("Students & Hobbyists", table_cell_bold),
            Paragraph("Cannot afford monthly subscriptions or cloud API fees to test music tools.", table_cell),
            Paragraph("<b>100% Free:</b> Operates with zero subscriptions, zero API keys, and zero developer portal approvals using public YouTube Music endpoints.", table_cell)
        ],
        [
            Paragraph("Software Developers & Programmers", table_cell_bold),
            Paragraph("GUI players consume high RAM/CPU and distract from code editors.", table_cell),
            Paragraph("<b>Distraction-Free CLI:</b> Instant background streaming via terminal or retro TUI, paired with automated focus and lo-fi playlist curation.", table_cell)
        ],
        [
            Paragraph("Multilingual & Regional Speakers", table_cell_bold),
            Paragraph("AI voice assistants fail to parse Indian languages and colloquial code-switching.", table_cell),
            Paragraph("<b>Native Regional Support:</b> Natively understands Hindi, Kannada, Telugu, Tamil, Bengali, Malayalam, Spanish, French, and Hinglish.", table_cell)
        ],
        [
            Paragraph("Accessibility & Hands-Free Users", table_cell_bold),
            Paragraph("Typing commands while working, cooking, or exercising is inconvenient.", table_cell),
            Paragraph("<b>Multilingual Voice Pipeline:</b> Microphone audio capture with precompiled Windows sounddevice drivers and spoken SAPI audio responses.", table_cell)
        ],
        [
            Paragraph("Academic Evaluators & Recruiters", table_cell_bold),
            Paragraph("Seeking real architectural depth, test coverage, and design patterns.", table_cell),
            Paragraph("<b>Enterprise Software Architecture:</b> Clean separation of concerns, Singleton, Strategy, Pydantic validation, SQLite persistence, and 33 passing unit tests.", table_cell)
        ]
    ]

    t_ben = Table(benefits_data, colWidths=[110, 150, 244])
    t_ben.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_ben)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 3: SYSTEM ARCHITECTURE & PROJECT FLOW
    # =========================================================================
    story.append(Paragraph("3. End-to-End System Architecture & Project Flow", h1_style))
    p_flow = """
    The system follows a strict unidirectional, decoupled request-response flow. The AI parser never interacts
    directly with external music services; all operations are mediated through a validated command dispatcher:
    """
    story.append(Paragraph(p_flow, body_style))

    flow_data = [
        [
            Paragraph("Stage #", table_header),
            Paragraph("Pipeline Stage", table_header),
            Paragraph("Technical Component", table_header),
            Paragraph("Operational Description & Output", table_header)
        ],
        [
            Paragraph("1", table_cell_bold),
            Paragraph("Input Capture", table_cell),
            Paragraph("CLI / Voice Listener", table_cell),
            Paragraph("Receives raw user input via terminal prompt or 16-bit 16kHz microphone stream via <code>sounddevice</code>.", table_cell)
        ],
        [
            Paragraph("2", table_cell_bold),
            Paragraph("Language Detection", table_cell),
            Paragraph("<code>LanguageDetector</code>", table_cell),
            Paragraph("Performs Unicode script inspection (Devanagari, Kannada, Telugu, Tamil, Bengali) and romanized token heuristics.", table_cell)
        ],
        [
            Paragraph("3", table_cell_bold),
            Paragraph("Context Resolution", table_cell),
            Paragraph("<code>ConversationManager</code>", table_cell),
            Paragraph("Checks multi-turn conversation memory, merges active language/genre clarification slots, and checks pending action confirmations.", table_cell)
        ],
        [
            Paragraph("4", table_cell_bold),
            Paragraph("Intent Parsing & NLU", table_cell),
            Paragraph("<code>IntentParser</code>", table_cell),
            Paragraph("Iteratively strips conversational preambles, classifies intent, extracts duration/artist/mood entities, and validates against <code>MusicIntent</code>.", table_cell)
        ],
        [
            Paragraph("5", table_cell_bold),
            Paragraph("Command Dispatching", table_cell),
            Paragraph("Dispatcher Layer", table_cell),
            Paragraph("Routes validated intent to discovery engine, playlist generator, or direct playback service based on validated schema.", table_cell)
        ],
        [
            Paragraph("6", table_cell_bold),
            Paragraph("Discovery & Curation", table_cell),
            Paragraph("<code>MusicDiscoveryEngine</code>", table_cell),
            Paragraph("Searches YouTube Music, ranks candidates with preference bonuses (+25 fav artist, +15 lang, -100 dislike), and balances artist diversity.", table_cell)
        ],
        [
            Paragraph("7", table_cell_bold),
            Paragraph("Playback & Media Keys", table_cell),
            Paragraph("<code>YouTubeMusicPlayback</code>", table_cell),
            Paragraph("Spawns non-blocking daemon stream launcher and dispatches global Windows media keys (<code>0xB3 Play/Pause</code>).", table_cell)
        ],
        [
            Paragraph("8", table_cell_bold),
            Paragraph("Multilingual Response", table_cell),
            Paragraph("<code>ResponseGenerator</code>", table_cell),
            Paragraph("Formulates natural conversational feedback in the user's detected language and triggers non-blocking SAPI5 speech synthesis.", table_cell)
        ]
    ]

    t_flow = Table(flow_data, colWidths=[35, 95, 120, 254])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: MODULAR COMPONENT BREAKDOWN
    # =========================================================================
    story.append(Paragraph("4. Technical Component & Subsystem Deep Dive", h1_style))

    story.append(Paragraph("4.1 Core Conversational AI Subsystem (<code>ai_engine/</code>)", h2_style))
    p_ai = """
    The AI engine processes natural language commands through structured, strongly-typed models:
    • <b>Pydantic Intent Validation (<code>intent_schema.py</code>):</b> Enforces rigorous data contracts. Supported intents: <code>PLAY_TRACK</code>, <code>PAUSE</code>, <code>RESUME</code>, <code>NEXT_TRACK</code>, <code>PREVIOUS_TRACK</code>, <code>SEARCH_TRACK</code>, <code>SEARCH_ARTIST</code>, <code>PLAY_ARTIST</code>, <code>CREATE_PLAYLIST</code>, <code>DISCOVER_MUSIC</code>, <code>MOOD_RECOMMENDATION</code>, <code>SIMILAR_MUSIC</code>, <code>CURRENTLY_PLAYING</code>.<br/>
    • <b>Iterative Preamble Stripping:</b> Advanced regex pipeline removes polite conversational openings (e.g. <i>'Can you please play'</i>, <i>'Bhai mujhe sunna hai'</i>, <i>'Nanage haadu beku'</i>) to reliably resolve exact entity names.<br/>
    • <b>Multilingual Response Generator (<code>response_generator.py</code>):</b> Synthesizes responses in English, Hindi, Hinglish, Kannada, Telugu, Tamil, Spanish, and French, avoiding robotic English-only replies.<br/>
    • <b>Multi-Turn Conversation Manager (<code>conversation_manager.py</code>):</b> Implements session history, auto-slot filling for pending questions, and two-phase confirmation gates for playlist creation.
    """
    story.append(Paragraph(p_ai, body_style))

    story.append(Paragraph("4.2 YouTube Music Service Integration (<code>youtube_music/</code>)", h2_style))
    p_yt = """
    Replaces deprecated Spotify dependencies with a robust, zero-cost architecture:
    • <b>Dual-Mode Architecture:</b> Operates in <i>Public Mode</i> out-of-the-box (requiring zero API keys or logins) and automatically unlocks <i>Authenticated Mode</i> if <code>oauth.json</code> is provided.<br/>
    • <b>In-Memory LRU Caching:</b> Caches search responses for 10 minutes in RAM, reducing repeated query latency from 1,500ms down to 0.1ms.<br/>
    • <b>Async Daemon Streaming & Virtual Media Keys:</b> Dispatches browser stream opening asynchronously to prevent CLI thread blocking, while operating-system virtual keys (<code>ctypes.windll.user32.keybd_event</code>) control system Play/Pause and Next/Previous globally.
    """
    story.append(Paragraph(p_yt, body_style))

    story.append(Paragraph("4.3 Music Intelligence & AI Playlist Generator (<code>music_engine/</code>)", h2_style))
    p_me = """
    • <b>Mood & Activity Classifier (<code>mood_classifier.py</code>):</b> Maps human context (coding, study, workout, sad, happy, chill, travel, sleep) into acoustic descriptors and curated search tags.<br/>
    • <b>Multi-Factor Track Ranker (<code>ranking.py</code>):</b> Scores candidate tracks based on favorite artist match (+25), preferred language match (+15), explicit user like (+30), and disliked penalty (-100). Enforces a 2-track maximum per artist to guarantee diversity.<br/>
    • <b>Time-Targeted Playlist Generator (<code>playlist_generator.py</code>):</b> Takes natural language duration targets (e.g. <i>'30-minute'</i>, <i>'2 hours'</i>), calculates exact cumulative runtimes using track <code>duration_seconds</code>, deduplicates titles, and returns a verified preview before dispatch.
    """
    story.append(Paragraph(p_me, body_style))

    story.append(Paragraph("4.4 Persistent User Profile & Memory (<code>memory/</code>)", h2_style))
    p_mem = """
    Persistent state is maintained in a local SQLite database (<code>musiq_ai.db</code>) managed through thread-safe context handlers:
    • <code>user_preferences</code>: Stores preferred language, favorite artists, genres, and moods.<br/>
    • <code>activity_preferences</code>: Maps recurring user habits (e.g. coding -> instrumental, workout -> energetic).<br/>
    • <code>track_feedback</code>: Stores likes and dislikes to permanently bias discovery scoring.<br/>
    • <code>playlist_history</code>: Records generated playlists, durations, and JSON video ID queues.
    """
    story.append(Paragraph(p_mem, body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: DATABASE SCHEMA & DATA CONTRACTS
    # =========================================================================
    story.append(Paragraph("5. Database Schema & Data Models", h1_style))
    schema_data = [
        [Paragraph("Table Name", table_header), Paragraph("Primary Key / Column", table_header), Paragraph("Data Type & Constraints", table_header), Paragraph("Purpose & Business Logic", table_header)],
        [Paragraph("user_preferences", table_cell_bold), Paragraph("pref_key", table_cell), Paragraph("TEXT PRIMARY KEY", table_cell), Paragraph("Stores user-configured language, artists list, genres list.", table_cell)],
        [Paragraph("activity_preferences", table_cell_bold), Paragraph("activity", table_cell), Paragraph("TEXT PRIMARY KEY", table_cell), Paragraph("Stores habitual mappings (e.g. coding -> instrumental lo-fi).", table_cell)],
        [Paragraph("track_feedback", table_cell_bold), Paragraph("id", table_cell), Paragraph("INTEGER AUTOINCREMENT", table_cell), Paragraph("Records track title, artist, and is_liked flag (1/0) for rank scoring.", table_cell)],
        [Paragraph("playlist_history", table_cell_bold), Paragraph("id", table_cell), Paragraph("INTEGER AUTOINCREMENT", table_cell), Paragraph("Records playlist name, target duration, track count, and video IDs JSON.", table_cell)]
    ]
    t_sch = Table(schema_data, colWidths=[100, 100, 110, 194])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_sch)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 6: MULTILINGUAL VERIFICATION MATRIX
    # =========================================================================
    story.append(Paragraph("6. Multilingual Verification & Command Matrix", h1_style))
    p_multi = "The following matrix reflects actual verified natural-language execution across all supported languages:"
    story.append(Paragraph(p_multi, body_style))

    multi_data = [
        [Paragraph("Language", table_header), Paragraph("Natural Language Command", table_header), Paragraph("Parsed Intent", table_header), Paragraph("System Action & Execution Output", table_header)],
        [Paragraph("Hindi", table_cell_bold), Paragraph("Mujhe Arijit Singh ke gaane sunne hain.", table_cell), Paragraph("PLAY_ARTIST", table_cell), Paragraph("Resolves artist 'Arijit Singh', streams top hit tracks on YouTube Music.", table_cell)],
        [Paragraph("Kannada", table_cell_bold), Paragraph("Nanage workout ge energetic songs beku.", table_cell), Paragraph("MOOD_RECOMMENDATION", table_cell), Paragraph("Detects Kannada-English, curates energetic workout anthems, prints track table.", table_cell)],
        [Paragraph("Telugu", table_cell_bold), Paragraph("Naaku peaceful music play cheyyi.", table_cell), Paragraph("MOOD_RECOMMENDATION", table_cell), Paragraph("Identifies Telugu language and peaceful mood; launches serene acoustic stream.", table_cell)],
        [Paragraph("Tamil", table_cell_bold), Paragraph("Enakku coding panna instrumental music venum.", table_cell), Paragraph("MOOD_RECOMMENDATION", table_cell), Paragraph("Identifies coding context and instrumental genre; streams lo-fi beats.", table_cell)],
        [Paragraph("Hinglish", table_cell_bold), Paragraph("Bhai coding ke liye kuch instrumental music chalao.", table_cell), Paragraph("MOOD_RECOMMENDATION", table_cell), Paragraph("Strips Hinglish preambles, resolves focus context, streams instrumental music.", table_cell)],
        [Paragraph("English", table_cell_bold), Paragraph("Create a 45-minute Hindi playlist for evening.", table_cell), Paragraph("CREATE_PLAYLIST", table_cell), Paragraph("Calculates ~2700s duration, curates tracks, asks user confirmation.", table_cell)],
        [Paragraph("Spanish", table_cell_bold), Paragraph("Reproducir musica relajante para dormir.", table_cell), Paragraph("MOOD_RECOMMENDATION", table_cell), Paragraph("Detects Spanish, resolves sleep/relaxing context, streams calming tracks.", table_cell)],
        [Paragraph("French", table_cell_bold), Paragraph("Jouer de la musique calme pour travailler.", table_cell), Paragraph("MOOD_RECOMMENDATION", table_cell), Paragraph("Detects French, resolves work/calm context, streams focus music.", table_cell)]
    ]

    t_multi = Table(multi_data, colWidths=[65, 175, 110, 154])
    t_multi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_multi)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 7: TESTING & QUALITY ASSURANCE
    # =========================================================================
    story.append(Paragraph("7. Automated Testing & Verification Suite", h1_style))
    p_test = """
    To guarantee production-grade stability, an enterprise-grade automated test suite was constructed under <code>tests/</code>.
    In compliance with engineering standards, all tests utilize mock fixtures, allowing the entire suite to run 100% offline
    without incurring API costs, requiring credentials, or depending on external network connectivity:
    """
    story.append(Paragraph(p_test, body_style))

    test_data = [
        [Paragraph("Test Module", table_header), Paragraph("Scope & Tested Functionality", table_header), Paragraph("Assertions & Checks", table_header), Paragraph("Result", table_header)],
        [Paragraph("test_multilingual.py", table_cell_bold), Paragraph("Unicode script & code-switching detection", table_cell), Paragraph("Devanagari, Kannada, Telugu, Tamil, Bengali, Hinglish, BCP-47 codes", table_cell), Paragraph("5 / 5 PASS", table_cell_bold)],
        [Paragraph("test_intent_parser.py", table_cell_bold), Paragraph("Pydantic schema validation & entity extraction", table_cell), Paragraph("Preamble stripping, duration math, multi-turn slots, confirmation", table_cell), Paragraph("9 / 9 PASS", table_cell_bold)],
        [Paragraph("test_music_search.py", table_cell_bold), Paragraph("YouTube Music normalization & caching", table_cell), Paragraph("Song metadata formatting, artist stats, local playlist curation", table_cell), Paragraph("4 / 4 PASS", table_cell_bold)],
        [Paragraph("test_playlist_generator.py", table_cell_bold), Paragraph("Time-targeted playlist budgeting", table_cell), Paragraph("Duration accumulation, format formatting, creation dispatch", table_cell), Paragraph("3 / 3 PASS", table_cell_bold)],
        [Paragraph("test_recommendations.py", table_cell_bold), Paragraph("Scoring algorithm & diversity filter", table_cell), Paragraph("Favorite artist boost (+25), dislike penalty (-100), artist diversity", table_cell), Paragraph("4 / 4 PASS", table_cell_bold)],
        [Paragraph("test_memory.py", table_cell_bold), Paragraph("SQLite persistent CRUD & feedback", table_cell), Paragraph("Language preferences, activity mappings, likes/dislikes persistence", table_cell), Paragraph("5 / 5 PASS", table_cell_bold)],
        [Paragraph("test_response_generator.py", table_cell_bold), Paragraph("Multilingual conversational response synthesis", table_cell), Paragraph("Regional string templates, iterative preamble stripping, search cache", table_cell), Paragraph("3 / 3 PASS", table_cell_bold)]
    ]

    t_test = Table(test_data, colWidths=[120, 140, 174, 70])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_test)

    summary_box = """
    <b>Testing Execution Benchmark:</b><br/>
    <code>python -m unittest discover tests</code><br/>
    <b>Total Tests:</b> 33 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Failures:</b> 0 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Errors:</b> 0 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Execution Runtime:</b> 0.358 seconds
    """
    story.append(Spacer(1, 6))
    story.append(Paragraph(summary_box, callout_style))
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 8: OPERATIONS MANUAL & CLI QUICKSTART
    # =========================================================================
    story.append(Paragraph("8. User Operations Manual & CLI Reference", h1_style))
    p_ops = "MUSIQ AI provides 5 distinct, interoperable operational interfaces:"
    story.append(Paragraph(p_ops, body_style))

    story.append(Paragraph("1. <b>Conversational AI Assistant (Primary Mode):</b> Run <code>python main.py ai</code>. Engage in multi-turn natural language dialogue across any supported language.", bullet_style))
    story.append(Paragraph("2. <b>Multilingual Voice Assistant:</b> Run <code>python main.py voice</code> or <code>python voiceActions.py</code>. Activate with <i>'Hello'</i> and speak naturally.", bullet_style))
    story.append(Paragraph("3. <b>Direct Terminal Subcommands:</b> Run <code>python main.py play &lt;song&gt;</code>, <code>python main.py pause</code>, <code>python main.py resume</code>, <code>python main.py artist-info &lt;artist&gt;</code>, or <code>python main.py get-playlists &lt;name&gt;</code>.", bullet_style))
    story.append(Paragraph("4. <b>Interactive Prompt Shell:</b> Run <code>python shell.py</code>. Features command history and tab-assisted auto-completion.", bullet_style))
    story.append(Paragraph("5. <b>Retro Terminal UI (TUI):</b> Run <code>python tui.py</code>. Full-screen retro dashboard displaying live progress bars and user playlist sidebars.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 9: ETHICAL COMPLIANCE & LEGAL SAFETY
    # =========================================================================
    story.append(Paragraph("9. Ethical Compliance, Copyright Safety & Policies", h1_style))
    p_eth = """
    MUSIQ AI was built with strict adherence to platform policies, intellectual property laws, and ethical API standards:
    • <b>Zero DRM Tampering / No Stream Decryption:</b> MUSIQ AI never downloads, decrypts, or redistributes copyrighted audio streams. Playback is natively orchestrated via the official YouTube Music web client.<br/>
    • <b>No Scraping of Restricted Private Endpoints:</b> Operates exclusively via supported public YouTube Music catalogue endpoints and sanctioned OAuth flows.<br/>
    • <b>Transparent User Privacy:</b> User memory and preferences are stored exclusively on the user's local disk in SQLite (<code>musiq_ai.db</code>); zero private listening data or conversation logs are transmitted to external servers.
    """
    story.append(Paragraph(p_eth, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Master PDF Report successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf()
