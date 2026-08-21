#!/usr/bin/env python3
"""Refresh GitHub metadata for curated toolbox repositories.

Metadata is an overlay. This script never edits human-curated catalog fields.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

API = "https://api.github.com"
API_VERSION = "2022-11-28"


class NotFound(Exception):
    pass


class GitHubAPI:
    def __init__(self, token: str | None = None, retries: int = 3):
        self.token = token or None
        self.retries = retries

    def get(self, path: str, *, allow_404: bool = False) -> Any:
        url = path if path.startswith("http") else f"{API}{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "embaya-open-source-toolbox",
            "X-GitHub-Api-Version": API_VERSION,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if exc.code == 404 and allow_404:
                    raise NotFound(url) from exc
                retry_after = exc.headers.get("Retry-After")
                remaining = exc.headers.get("X-RateLimit-Remaining")
                if attempt < self.retries and (exc.code in {429, 502, 503, 504} or (exc.code == 403 and (retry_after or remaining == "0"))):
                    delay = int(retry_after or 2 ** attempt)
                    time.sleep(max(1, min(delay, 60)))
                    continue
                body = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"GitHub API {exc.code} for {url}: {body[:500]}") from exc
            except urllib.error.URLError as exc:
                if attempt < self.retries:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"GitHub API request failed for {url}: {exc}") from exc
        raise RuntimeError(f"GitHub API request failed for {url}")


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def days_since(value: str | None, now: datetime) -> int | None:
    dt = parse_dt(value)
    if dt is None:
        return None
    return max(0, (now - dt).days)


def maintenance_status(repo: dict[str, Any], now: datetime) -> str:
    if repo.get("availability") == "not_found": return "MISSING"
    if repo.get("availability") == "inaccessible": return "INACCESSIBLE"
    if repo.get("disabled"): return "DISABLED"
    if repo.get("archived"): return "ARCHIVED"
    age = days_since(repo.get("pushed_at"), now)
    if age is None: return "UNKNOWN"
    if age <= 90: return "ACTIVE"
    if age <= 365: return "SLOW"
    if age <= 730: return "STALE"
    return "DORMANT"


def activity_score(repo: dict[str, Any], now: datetime) -> int:
    if repo.get("archived") or repo.get("disabled") or repo.get("availability") in {"not_found", "inaccessible"}:
        return 0
    push_age = days_since(repo.get("pushed_at"), now)
    update_age = days_since(repo.get("updated_at"), now)
    release_age = days_since((repo.get("latest_release") or {}).get("published_at"), now)

    def freshness(age: int | None, bands: list[tuple[int, int]], default: int = 0) -> int:
        if age is None: return default
        for max_days, points in bands:
            if age <= max_days: return points
        return default

    score = freshness(push_age, [(30, 60), (90, 52), (180, 44), (365, 34), (730, 20)], 8)
    score += freshness(update_age, [(30, 20), (90, 16), (365, 10), (730, 5)], 0)
    score += freshness(release_age, [(90, 20), (365, 15), (730, 8)], 0)
    return max(0, min(100, score))


def maturity_score(repo: dict[str, Any], now: datetime) -> int:
    if repo.get("availability") in {"not_found", "inaccessible"}: return 0
    score = 0
    created_age = days_since(repo.get("created_at"), now) or 0
    if created_age >= 1095: score += 15
    elif created_age >= 730: score += 13
    elif created_age >= 365: score += 10
    elif created_age >= 180: score += 6
    else: score += 3
    stars = max(0, int(repo.get("stargazers_count") or 0))
    forks = max(0, int(repo.get("forks_count") or 0))
    score += min(25, round(math.log10(stars + 1) * 6))
    score += min(15, round(math.log10(forks + 1) * 5))
    if repo.get("license"): score += 15
    if repo.get("latest_release"): score += 15
    if repo.get("has_issues"): score += 5
    if repo.get("has_discussions"): score += 5
    if repo.get("homepage"): score += 5
    if repo.get("archived"): score -= 25
    if repo.get("disabled"): score -= 40
    return max(0, min(100, score))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists(): return []
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try: rows.append(json.loads(line))
        except json.JSONDecodeError as exc: raise RuntimeError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
    return rows


def catalog_repositories(catalog_dir: Path) -> list[str]:
    names = set()
    for path in sorted(catalog_dir.glob("*.jsonl")):
        for row in read_jsonl(path):
            if row.get("repository"): names.add(str(row["repository"]))
    return sorted(names, key=str.lower)


def fetch_one(api: GitHubAPI, repository: str, now: datetime) -> dict[str, Any]:
    try:
        details = api.get(f"/repos/{repository}", allow_404=True)
    except NotFound:
        return {"repository": repository, "availability": "not_found", "maintenance_status": "MISSING", "activity_score": 0, "maturity_score": 0}
    except RuntimeError as exc:
        return {"repository": repository, "availability": "inaccessible", "refresh_error": str(exc), "maintenance_status": "INACCESSIBLE", "activity_score": 0, "maturity_score": 0}

    latest_release = None
    try:
        release = api.get(f"/repos/{repository}/releases/latest", allow_404=True)
        latest_release = {
            "tag_name": release.get("tag_name"), "name": release.get("name"),
            "published_at": release.get("published_at"), "html_url": release.get("html_url"),
            "prerelease": bool(release.get("prerelease")),
        }
    except (NotFound, RuntimeError):
        pass

    license_obj = details.get("license") or {}
    row = {
        "repository": repository,
        "resolved_repository": details.get("full_name") or repository,
        "availability": "available",
        "html_url": details.get("html_url"),
        "description": details.get("description"),
        "homepage": details.get("homepage"),
        "language": details.get("language"),
        "license": license_obj.get("spdx_id") or license_obj.get("key"),
        "topics": sorted(details.get("topics") or []),
        "visibility": details.get("visibility"),
        "archived": bool(details.get("archived")),
        "disabled": bool(details.get("disabled")),
        "fork": bool(details.get("fork")),
        "stargazers_count": details.get("stargazers_count") or 0,
        "forks_count": details.get("forks_count") or 0,
        "subscribers_count": details.get("subscribers_count") or 0,
        "open_issues_count": details.get("open_issues_count") or 0,
        "size_kb": details.get("size") or 0,
        "default_branch": details.get("default_branch"),
        "has_issues": bool(details.get("has_issues")),
        "has_discussions": bool(details.get("has_discussions")),
        "created_at": details.get("created_at"),
        "updated_at": details.get("updated_at"),
        "pushed_at": details.get("pushed_at"),
        "latest_release": latest_release,
    }
    row["maintenance_status"] = maintenance_status(row, now)
    row["activity_score"] = activity_score(row, now)
    row["maturity_score"] = maturity_score(row, now)
    return row


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8") == text: return
    path.write_text(text, encoding="utf-8")


def build_summary(rows: list[dict[str, Any]]) -> str:
    statuses: dict[str, int] = {}
    for row in rows:
        status = row.get("maintenance_status") or "UNKNOWN"
        statuses[status] = statuses.get(status, 0) + 1
    lines = ["# GitHub metadata summary", "", f"Repositories: **{len(rows)}**", "", "| Maintenance status | Count |", "|---|---:|"]
    for status in sorted(statuses): lines.append(f"| {status} | {statuses[status]} |")
    lines += ["", "Scores are deterministic heuristics for navigation only. They are not production-readiness guarantees and never change curated priority automatically.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh GitHub metadata overlay for toolbox repositories")
    parser.add_argument("--catalog-dir", type=Path, default=Path("catalog"))
    parser.add_argument("--output", type=Path, default=Path("metadata/github.jsonl"))
    parser.add_argument("--summary", type=Path, default=Path("metadata/summary.md"))
    parser.add_argument("--result", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN", "").strip() or os.getenv("TOOLBOX_GITHUB_TOKEN", "").strip() or None
    repositories = catalog_repositories(args.catalog_dir)
    now = datetime.now(timezone.utc)
    rows = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        future_map = {pool.submit(fetch_one, GitHubAPI(token), repo, now): repo for repo in repositories}
        for future in as_completed(future_map):
            repo = future_map[future]
            try: rows.append(future.result())
            except Exception as exc:
                rows.append({"repository": repo, "availability": "inaccessible", "refresh_error": str(exc), "maintenance_status": "INACCESSIBLE", "activity_score": 0, "maturity_score": 0})

    rows.sort(key=lambda r: str(r["repository"]).lower())
    write_jsonl(args.output, rows)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    summary_text = build_summary(rows)
    if not args.summary.exists() or args.summary.read_text(encoding="utf-8") != summary_text:
        args.summary.write_text(summary_text, encoding="utf-8")

    result = {
        "catalog_repositories": len(repositories), "metadata_rows": len(rows),
        "available": sum(1 for r in rows if r.get("availability") == "available"),
        "not_found": sum(1 for r in rows if r.get("availability") == "not_found"),
        "inaccessible": sum(1 for r in rows if r.get("availability") == "inaccessible"),
    }
    if args.result:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
