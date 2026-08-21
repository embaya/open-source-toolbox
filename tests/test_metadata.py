import importlib.util
import unittest
from datetime import datetime, timezone
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "refresh_metadata.py"
spec = importlib.util.spec_from_file_location("refresh_metadata", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)
NOW = datetime(2026, 8, 22, tzinfo=timezone.utc)


class MetadataTests(unittest.TestCase):
    def test_maintenance_status_by_push_age(self):
        base = {"availability": "available", "archived": False, "disabled": False}
        self.assertEqual(mod.maintenance_status({**base, "pushed_at": "2026-08-01T00:00:00Z"}, NOW), "ACTIVE")
        self.assertEqual(mod.maintenance_status({**base, "pushed_at": "2026-01-01T00:00:00Z"}, NOW), "SLOW")
        self.assertEqual(mod.maintenance_status({**base, "pushed_at": "2025-01-01T00:00:00Z"}, NOW), "STALE")
        self.assertEqual(mod.maintenance_status({**base, "pushed_at": "2020-01-01T00:00:00Z"}, NOW), "DORMANT")

    def test_archived_overrides_activity(self):
        row = {"availability": "available", "archived": True, "disabled": False, "pushed_at": "2026-08-20T00:00:00Z"}
        self.assertEqual(mod.maintenance_status(row, NOW), "ARCHIVED")
        self.assertEqual(mod.activity_score(row, NOW), 0)

    def test_scores_are_bounded(self):
        row = {
            "availability": "available", "archived": False, "disabled": False,
            "created_at": "2015-01-01T00:00:00Z", "updated_at": "2026-08-20T00:00:00Z",
            "pushed_at": "2026-08-20T00:00:00Z", "stargazers_count": 500000,
            "forks_count": 50000, "license": "MIT",
            "latest_release": {"published_at": "2026-08-01T00:00:00Z"},
            "has_issues": True, "has_discussions": True, "homepage": "https://example.com",
        }
        self.assertGreaterEqual(mod.activity_score(row, NOW), 0)
        self.assertLessEqual(mod.activity_score(row, NOW), 100)
        self.assertGreaterEqual(mod.maturity_score(row, NOW), 0)
        self.assertLessEqual(mod.maturity_score(row, NOW), 100)


if __name__ == "__main__":
    unittest.main()
