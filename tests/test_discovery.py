import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "discover_repositories.py"
spec = importlib.util.spec_from_file_location("discover_repositories", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)


class DiscoveryTests(unittest.TestCase):
    def test_aggregate_deduplicates_star_and_fork_to_canonical(self):
        stars = [{"full_name": "upstream/project", "fork": False}]
        forks = [{"full_name": "embaya/project", "fork": True}]

        def resolver(repo):
            return ("upstream/project", None) if repo["fork"] else (repo["full_name"], None)

        result = mod.aggregate_sources(stars, forks, resolver)
        row = result["upstream/project"]
        self.assertTrue(row["starred"])
        self.assertTrue(row["forked"])
        self.assertEqual(row["source_entries"], ["embaya/project", "upstream/project"])

    def test_merge_pending_preserves_human_fields(self):
        existing = [{
            "repository": "foo/bar",
            "status": "pending_review",
            "detected_at": "2026-08-20",
            "note": "manual note",
            "source_active": True,
        }]
        discovered = {
            "foo/bar": {
                "repository": "foo/bar",
                "starred": True,
                "forked": False,
                "source_entries": ["foo/bar"],
            },
            "new/tool": {
                "repository": "new/tool",
                "starred": False,
                "forked": True,
                "source_entries": ["embaya/tool"],
            },
        }
        rows, new_count, _ = mod.merge_pending(existing, discovered, set(), "2026-08-22")
        by_repo = {r["repository"]: r for r in rows}
        self.assertEqual(new_count, 1)
        self.assertEqual(by_repo["foo/bar"]["note"], "manual note")
        self.assertEqual(by_repo["new/tool"]["status"], "pending_review")

    def test_catalog_entries_are_not_added_to_pending(self):
        discovered = {
            "already/cataloged": {
                "repository": "Already/Cataloged",
                "starred": True,
                "forked": True,
                "source_entries": ["Already/Cataloged"],
            }
        }
        rows, new_count, _ = mod.merge_pending([], discovered, {"already/cataloged"}, "2026-08-22")
        self.assertEqual(rows, [])
        self.assertEqual(new_count, 0)


if __name__ == "__main__":
    unittest.main()
