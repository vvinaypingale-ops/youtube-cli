import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from youtube_music.client import get_ytmusic_client
from youtube_music.search import YouTubeMusicSearch
from youtube_music.playback import YouTubeMusicPlayback
from youtube_music.playlist import YouTubeMusicPlaylist
from youtube_music.authentication import print_auth_info

from ai_engine.intent_parser import IntentParser
from ai_engine.intent_schema import IntentType
from ai_engine.conversation_manager import ConversationManager
from ai_engine.language_detector import LanguageDetector
from ai_engine.response_generator import ResponseGenerator

from music_engine.discovery import MusicDiscoveryEngine
from music_engine.playlist_generator import PlaylistGenerator
from memory.user_preferences import UserPreferencesManager
from memory.feedback import FeedbackManager

console = Console()
app = typer.Typer(
    help="MUSIQ AI – Intelligent Multilingual Music Assistant (Powered by YouTube Music)"
)

# Services
search_service = YouTubeMusicSearch()
playback_service = YouTubeMusicPlayback(search_service)
playlist_service = YouTubeMusicPlaylist()
discovery_engine = MusicDiscoveryEngine(search_service)
playlist_gen = PlaylistGenerator(discovery_engine, playlist_service)
intent_parser = IntentParser()
conv_manager = ConversationManager()
prefs_manager = UserPreferencesManager()
feedback_manager = FeedbackManager()
lang_detector = LanguageDetector()
resp_gen = ResponseGenerator()


@app.command()
def ai():
    """Launch the interactive conversational MUSIQ AI multilingual assistant."""
    console.print(
        Panel.fit(
            """[bold cyan]░█▀▄▀█░█░█░█▀▀░▀█▀░█▀▀░░░█▀▀░█░░░▀█▀
░█░▀░█░█░█░▀▀█░░█░░█░░░░░█░░░█░░░░█░
░▀░░░▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀[/bold cyan]
[bold green]MUSIQ AI – Intelligent Multilingual Music Assistant[/bold green]
[dim]Supported: English, Hindi, Kannada, Telugu, Tamil, Malayalam, Bengali, Spanish, French, Hinglish[/dim]
[dim]Type 'help' for tips, 'prefs' for preferences, or 'exit' to quit.[/dim]""",
            title="Interactive AI Mode"
        )
    )

    console.print("[bold yellow]MUSIQ AI:[/bold yellow] Hello! Your multilingual music assistant is ready. How can I help you today?")

    while True:
        try:
            user_input = console.input("\n[bold cyan]You > [/bold cyan]").strip()
            if not user_input:
                continue

            low = user_input.lower()
            if low in ["exit", "quit", "bye", "band karo"]:
                console.print("[bold yellow]MUSIQ AI:[/bold yellow] Goodbye! Enjoy your music. 👋")
                break

            if low == "help":
                _show_ai_help()
                continue

            if low in ["prefs", "preferences"]:
                _show_preferences()
                continue

            # Process with AI Intent Engine
            _handle_ai_turn(user_input)

        except KeyboardInterrupt:
            console.print("\n[bold yellow]MUSIQ AI:[/bold yellow] Session ended. Goodbye! 👋")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


def _handle_ai_turn(user_input: str):
    detected_lang = lang_detector.detect_language(user_input)
    lang_name = lang_detector.get_language_display_name(detected_lang)

    intent = intent_parser.parse(user_input)
    intent = conv_manager.handle_followup_or_merge(user_input, intent)

    console.print(f"[dim]🌐 Language: {lang_name} | Intent: {intent.intent.value}[/dim]")

    if intent.intent == IntentType.PLAY_TRACK:
        query = intent.song_title or intent.query or user_input
        track = playback_service.play_track(query)
        if track:
            msg = resp_gen.format(detected_lang, "playing_track", title=track['title'], artist=track['artist'])
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")
        else:
            msg = resp_gen.format(detected_lang, "not_found", query=query)
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.PLAY_ARTIST:
        artist = intent.artist or intent.query
        msg = resp_gen.format(detected_lang, "playing_artist", artist=artist)
        console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")
        playback_service.play_track(f"{artist} top songs")

    elif intent.intent == IntentType.MOOD_RECOMMENDATION:
        with console.status("[bold cyan]Curating tracks...[/bold cyan]"):
            disc = discovery_engine.discover_music(
                mood=intent.mood,
                activity=intent.activity,
                language=intent.language,
                genre=intent.genre,
                artist=intent.artist,
                limit=6
            )

        tracks = disc.get("tracks", [])
        if tracks:
            top_track = tracks[0]
            ctx = f"{intent.language or ''} {intent.mood or intent.activity or 'music'}".strip()
            msg = resp_gen.format(detected_lang, "mood_recommendation", context=ctx, title=top_track['title'], artist=top_track['artist'])
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")
            _display_track_table(tracks)

            # Auto-play the top curated match
            playback_service.play_track(top_track)
        else:
            msg = resp_gen.format(detected_lang, "not_found", query=user_input)
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.CREATE_PLAYLIST:
        # Check if this is confirming an existing proposed plan
        if not intent.requires_confirmation and hasattr(conv_manager, "last_plan") and conv_manager.last_plan:
            plan = conv_manager.last_plan
            res = playlist_gen.create_playlist(plan)
            msg = resp_gen.format(detected_lang, "playlist_created", name=plan['playlist_name'], count=plan['track_count'], duration=plan['total_duration_formatted'])
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")
            console.print(f"🌐 Stream Link: {res['url']}")
            conv_manager.last_plan = None
            if plan.get("tracks"):
                playback_service.play_track(plan["tracks"][0])
        else:
            with console.status("[bold cyan]Curating playlist tracks...[/bold cyan]"):
                plan = playlist_gen.plan_playlist(
                    name=intent.playlist_name,
                    duration_minutes=intent.duration_minutes or 30,
                    mood=intent.mood,
                    activity=intent.activity,
                    language=intent.language,
                    genre=intent.genre
                )

            if plan.get("success"):
                console.print(f"\n[bold green]📋 Playlist Proposed:[/bold green] [bold]{plan['playlist_name']}[/bold]")
                console.print(f"⏱️ Target: {plan['target_minutes']}m | Actual: {plan['total_duration_formatted']} ({plan['track_count']} tracks)")
                _display_track_table(plan["tracks"][:10])

                conv_manager.last_plan = plan
                conv_manager.set_pending_confirmation(
                    action="CREATE_PLAYLIST",
                    data={"playlist_name": plan["playlist_name"], "duration_minutes": plan["target_minutes"]},
                    prompt=f"Should I create '{plan['playlist_name']}'?"
                )
                msg = resp_gen.format(detected_lang, "playlist_proposed", name=plan['playlist_name'], count=plan['track_count'], duration=plan['total_duration_formatted'])
                console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")
            else:
                msg = resp_gen.format(detected_lang, "not_found", query=user_input)
                console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.PAUSE:
        playback_service.pause()
        msg = resp_gen.format(detected_lang, "paused")
        console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.RESUME:
        playback_service.resume()
        msg = resp_gen.format(detected_lang, "resumed")
        console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.NEXT_TRACK:
        playback_service.next_track()
        msg = resp_gen.format(detected_lang, "next")
        console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.PREVIOUS_TRACK:
        playback_service.previous_track()
        msg = resp_gen.format(detected_lang, "prev")
        console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    elif intent.intent == IntentType.CURRENTLY_PLAYING:
        curr = playback_service.get_current_playing()
        if curr:
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] 🎵 Currently playing: [bold]{curr['title']}[/bold] by [bold]{curr['artist']}[/bold] ({curr['progress']}s / {curr['duration']}s)")
        else:
            console.print("[bold yellow]MUSIQ AI:[/bold yellow] Nothing is currently tracked as playing.")

    elif intent.intent == IntentType.SIMILAR_MUSIC:
        target = intent.artist or intent.query
        with console.status(f"[bold cyan]Finding tracks similar to '{target}'...[/bold cyan]"):
            sim = discovery_engine.find_similar(target, limit=6)
        tracks = sim.get("tracks", [])
        if tracks:
            top = tracks[0]
            msg = resp_gen.format(detected_lang, "similar", target=target, title=top['title'], artist=top['artist'])
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")
            _display_track_table(tracks)
            playback_service.play_track(top)
        else:
            msg = resp_gen.format(detected_lang, "not_found", query=target)
            console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {msg}")

    else:
        prompt = intent.clarification_prompt or "Could you clarify which song, artist, or mood you want to hear?"
        console.print(f"[bold yellow]MUSIQ AI:[/bold yellow] {prompt}")


def _display_track_table(tracks: list):
    table = Table(title="Recommended Tracks", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Track Title", style="bold cyan")
    table.add_column("Artist", style="green")
    table.add_column("Duration", style="yellow")

    for i, t in enumerate(tracks, 1):
        dur = t.get("duration", "3:30")
        table.add_row(str(i), t.get("title", ""), t.get("artist", ""), str(dur))

    console.print(table)


def _show_preferences():
    all_prefs = prefs_manager.get_all_preferences()
    table = Table(title="Stored User Preferences", show_header=True, header_style="bold yellow")
    table.add_column("Category", style="cyan")
    table.add_column("Setting", style="green")

    table.add_row("Preferred Language", all_prefs.get("preferred_language", "None"))
    table.add_row("Favorite Artists", ", ".join(all_prefs.get("favorite_artists", [])) or "None")
    table.add_row("Favorite Genres", ", ".join(all_prefs.get("favorite_genres", [])) or "None")

    for act, details in all_prefs.get("activities", {}).items():
        table.add_row(f"Activity: {act}", f"Genre: {details.get('genre', 'any')}, Mood: {details.get('mood', 'any')}")

    console.print(table)


def _show_ai_help():
    console.print("""
[bold green]Example Multilingual Requests:[/bold green]
  • [bold]Hindi:[/bold] "Mujhe Arijit Singh ke gaane sunne hain."
  • [bold]Kannada:[/bold] "Nanage workout ge energetic songs beku."
  • [bold]Telugu:[/bold] "Naaku peaceful music play cheyyi."
  • [bold]Tamil:[/bold] "Enakku coding panna instrumental music venum."
  • [bold]Hinglish:[/bold] "Bhai coding ke liye kuch instrumental music chalao."
  • [bold]English:[/bold] "Play something relaxing."
  • [bold]Playlist:[/bold] "Create a 45-minute Hindi playlist for evening."
  • [bold]Similar:[/bold] "Play music similar to Coldplay."
  • [bold]Controls:[/bold] "Pause", "Resume", "Next song", "What is playing?"
""")


# ==========================================
# STANDARD CLI COMMANDS (Preserved)
# ==========================================

@app.command()
def authenticate():
    """Display YouTube Music authentication and session status."""
    print_auth_info()

@app.command()
def play(song_name: str):
    """Search and play a song on YouTube Music."""
    playback_service.play_track(song_name)

@app.command()
def pause():
    """Toggle Play / Pause."""
    playback_service.pause()

@app.command()
def resume():
    """Resume playback."""
    playback_service.resume()

@app.command()
def next_song():
    """Skip to next track."""
    playback_service.next_track()

@app.command()
def artist_info(artist_name: str):
    """Fetch details and stats for an artist."""
    artists = search_service.search_artists(artist_name, limit=3)
    if artists:
        console.print(f"\n🔍 Search Results for '[bold green]{artist_name}[/bold green]':")
        for a in artists:
            console.print(f"🎤 [bold]{a['name']}[/bold] | Subscribers: {a['subscribers']}")
            if a.get('url'):
                console.print(f"   🌐 {a['url']}")
    else:
        console.print(f"❌ Artist '{artist_name}' not found.")

@app.command()
def add(data: list[str]):
    """Queue songs to add to a playlist: add song1 song2 playlist_name"""
    if len(data) < 2:
        console.print("Provide at least 1 song with playlist name (e.g. add song1 song2 playlist_name)")
        return
    pl_name = data[-1]
    songs = data[:-1]
    console.print(f"📁 Target Playlist: [bold]{pl_name}[/bold]")
    for s in songs:
        track = search_service.search_songs(s, limit=1)
        if track:
            console.print(f"✅ Queued '{track[0]['title']}' by {track[0]['artist']}")

@app.command()
def play_playlist(link: str):
    """Play a YouTube Music playlist by URL or name."""
    playlist_service.open_playlist(link)

@app.command()
def get_playlists(name: str):
    """Search for a playlist by name."""
    playlists = search_service.search_playlists(name, limit=5)
    for p in playlists:
        console.print(f"📃 [bold]{p['title']}[/bold] by {p['author']} ({p.get('item_count', '?')} tracks)")
        console.print(f"   🌐 {p['url']}")

@app.command()
def voice():
    """Launch the hands-free voice assistant."""
    from voice.voice_assistant import VoiceAssistant
    assistant = VoiceAssistant()
    assistant.run_loop()


if __name__ == "__main__":
    app()
