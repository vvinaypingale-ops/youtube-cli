import unittest
from unittest.mock import MagicMock, patch
from youtube_music.search import YouTubeMusicSearch
from youtube_music.playlist import YouTubeMusicPlaylist
from youtube_music.playback import YouTubeMusicPlayback

class TestYouTubeMusicIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_yt = MagicMock()
        self.search = YouTubeMusicSearch(yt=self.mock_yt)
        self.playback = YouTubeMusicPlayback(search_engine=self.search)
        self.playlist = YouTubeMusicPlaylist(yt=self.mock_yt)

    def test_search_songs_normalization(self):
        self.mock_yt.search.return_value = [
            {
                "title": "Kesariya",
                "artists": [{"name": "Arijit Singh"}],
                "videoId": "BddP6PYo2gs",
                "duration": "4:28",
                "duration_seconds": 268,
                "album": {"name": "Brahmastra"},
                "thumbnails": [{"url": "http://thumb.jpg"}]
            }
        ]

        tracks = self.search.search_songs("Kesariya", limit=1)
        self.assertEqual(len(tracks), 1)
        track = tracks[0]
        self.assertEqual(track["title"], "Kesariya")
        self.assertEqual(track["artist"], "Arijit Singh")
        self.assertEqual(track["video_id"], "BddP6PYo2gs")
        self.assertEqual(track["duration_seconds"], 268)

    def test_search_artists(self):
        self.mock_yt.search.return_value = [
            {
                "artist": "Arijit Singh",
                "browseId": "UC6nS87pD2jC9660i788_0aA",
                "thumbnails": [{"url": "http://artist.jpg"}]
            }
        ]
        self.mock_yt.get_artist.return_value = {"subscribers": "40M"}

        artists = self.search.search_artists("Arijit Singh", limit=1)
        self.assertEqual(len(artists), 1)
        self.assertEqual(artists[0]["name"], "Arijit Singh")
        self.assertEqual(artists[0]["subscribers"], "40M")

    def test_create_local_playlist(self):
        tracks = [
            {"title": "Song 1", "artist": "Artist 1", "video_id": "vid1", "duration_seconds": 180},
            {"title": "Song 2", "artist": "Artist 2", "video_id": "vid2", "duration_seconds": 200}
        ]
        result = self.playlist.create_playlist("Workout Mix", "Energetic tracks", tracks)
        self.assertTrue(result["success"])
        self.assertEqual(result["title"], "Workout Mix")
        self.assertEqual(result["track_count"], 2)
        self.assertEqual(result["duration_seconds"], 380)
        self.assertIn("watch_videos", result["url"])

    @patch("webbrowser.open")
    def test_playback_metadata_tracking(self, mock_browser):
        track_dict = {
            "title": "Believer",
            "artist": "Imagine Dragons",
            "video_id": "7wtfhZwyrcc",
            "duration_seconds": 204,
            "duration": "3:24"
        }
        self.playback.play_track(track_dict)
        current = self.playback.get_current_playing()
        self.assertIsNotNone(current)
        self.assertEqual(current["title"], "Believer")
        self.assertEqual(current["artist"], "Imagine Dragons")
        self.assertEqual(current["video_id"], "7wtfhZwyrcc")

if __name__ == "__main__":
    unittest.main()
