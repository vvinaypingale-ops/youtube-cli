import unittest
from unittest.mock import MagicMock
from music_engine.playlist_generator import PlaylistGenerator

class TestPlaylistGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_discovery = MagicMock()
        self.mock_playlist_service = MagicMock()
        self.generator = PlaylistGenerator(
            discovery_engine=self.mock_discovery,
            playlist_service=self.mock_playlist_service
        )

    def test_duration_formatting(self):
        self.assertEqual(self.generator.format_duration(1800), "30m 0s")
        self.assertEqual(self.generator.format_duration(3660), "1h 1m")
        self.assertEqual(self.generator.format_duration(215), "3m 35s")

    def test_playlist_planning_target_duration(self):
        # 10 mock candidate tracks (each ~200 seconds)
        mock_tracks = [
            {"title": f"Song {i}", "artist": f"Artist {i % 4}", "video_id": f"vid_{i}", "duration_seconds": 200}
            for i in range(15)
        ]
        self.mock_discovery.discover_music.return_value = {
            "tracks": mock_tracks,
            "query": "Hindi relaxing",
            "explanation": "Test explanation"
        }

        # Request 10-minute playlist (= 600 seconds)
        plan = self.generator.plan_playlist(
            name="Evening Relax",
            duration_minutes=10,
            mood="relaxing",
            language="Hindi"
        )

        self.assertTrue(plan["success"])
        self.assertEqual(plan["playlist_name"], "Evening Relax")
        # 3 tracks * 200s = 600s
        self.assertEqual(plan["track_count"], 3)
        self.assertEqual(plan["total_duration_seconds"], 600)

    def test_playlist_creation_dispatch(self):
        mock_plan = {
            "success": True,
            "playlist_name": "Coding Focus",
            "description": "Instrumental lo-fi",
            "tracks": [
                {"title": "Track 1", "artist": "Artist 1", "video_id": "v1", "duration_seconds": 180}
            ]
        }
        self.mock_playlist_service.create_playlist.return_value = {
            "success": True,
            "id": "local_180",
            "url": "https://www.youtube.com/watch_videos?video_ids=v1",
            "track_count": 1
        }

        result = self.generator.create_playlist(mock_plan)
        self.assertTrue(result["success"])
        self.mock_playlist_service.create_playlist.assert_called_once()

if __name__ == "__main__":
    unittest.main()
