#!/usr/bin/env python3
"""Discover repositories from GitHub Stars + owned forks without touching curated catalog data."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

API = "https://api.github.com"
API_VERSION = "2022-11-28"


class GitHubAPI:
    def __init__(self, token: str | None = None):
        self.token = token or None
        self.cache: dict[str, dict[str, Any]] = {}

    def _request(self, path: str) -> tuple[Any, dict[str, str]]:
        url = path if path.startswith("http") else f"{API}{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "embaya-open-source-toolbox",
            "X-GitHub-Api-Version": API_VERSION,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.load(response)
                response_headers = {k.lower(): v for k, v in response.headers.items()}
                return data, response_headers
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API {exc.code} for {url}: {body[:500]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"GitHub API request failed for {url}: {exc}") from exc

    def get(self, path: str) -> Any:
        data, _ = self._request(path)
        return data

    def paginate(self, path: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        url = path
        while url:
            data, headers = self._request(url)
            if not isinstance(data, list):
                raise RuntimeError(f"Expected a list from GitHub API for {url}")
            items.extend(data)
            url = next_link(headers.get("link", ""))
        return items

    def repo_details(self, full_name: str) -> dict[str, Any]:
        if full_name not in self.cache:
            self.cache[full_name] = self.get(f"/repos/{full_name}")
        return self.cache[full_name]


def next_link(link_header: str) -> str:
    for part in link_header.split(","):
        section = part.strip().split(";")
        if len(section) < 2:
            continue
        url = section[0].strip().strip("<>")
        rels = ";".join(section[1:])
        if 'rel="next"' in rels:
            return url
    return ""


def utc_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise RuntimeError(f"{path}:{lineno}: expected JSON object")
        rows.append(row)
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def load_catalog(catalog_dir: Path) -> set[str]:
    repositories: set[str] = set()
    for path in sorted(catalog_dir.glob("*.jsonl")):
        for row in read_jsonl(path):
            repo = row.get("repository")
            if repo:
                repositories.add(str(repo).lower())
    return repositories


def canonical_from_details(details: dict[str, Any]) -> str:
    source = details.get("source") or {}
    parent = details.get("parent") or {}
    return source.get("full_name") or parent.get("full_name") or details.get("full_name")


def resolve_repo(api: GitHubAPI, repo: dict[str, Any]) -> tuple[str, str | None]:
    full_name = repo.get("full_name")
    if not full_name:
        raise RuntimeError("GitHub repository object missing full_name")
    if not repo.get("fork"):
        return full_name, None
    try:
        details = api.repo_details(full_name)
        return canonical_from_details(details) or full_name, None
    except RuntimeError as exc:
        # Keep inaccessible/blocked forks rather than losing them.
        return full_name, str(exc)


def aggregate_sources(stars: Iterable[dict[str, Any]], forks: Iterable[dict[str, Any]], resolver) -> dict[str, dict[str, Any]]:
    aggregated: dict[str, dict[str, Any]] = {}

    def add(repo: dict[str, Any], source_type: str) -> None:
        canonical, resolution_error = resolver(repo)
        key = canonical.lower()
        entry = aggregated.setdefault(key, {
            "repository": canonical,
            "starred": False,
            "forked": False,
            "source_entries": [],
            "resolution_errors": [],
        })
        entry[source_type] = True
        source_name = repo.get("full_name")
        if source_name and source_name not in entry["source_entries"]:
            entry["source_entries"].append(source_name)
        if resolution_error and resolution_error not in entry["resolution_errors"]:
            entry["resolution_errors"].append(resolution_error)

    for repo in stars:
        add(repo, "starred")
    for repo in forks:
        add(repo, "forked")

    for entry in aggregated.values():
        entry["source_entries"] = sorted(entry["source_entries"], key=str.lower)
        if not entry["resolution_errors"]:
            entry.pop("resolution_errors")
    return aggregated


def merge_pending(current_pending: list[dict[str, Any]], discovered: dict[str, dict[str, Any]], catalog_repositories: set[str], today: str) -> tuple[list[dict[str, Any]], int, int]:
    existing = {str(row.get("repository", "")).lower(): dict(row) for row in current_pending if row.get("repository")}
    new_count = 0
    reactivated_count = 0

    for key, source in discovered.items():
        if key in catalog_repositories:
            continue
        if key not in existing:
            existing[key] = {
                "repository": source["repository"],
                "url": f"https://github.com/{source['repository']}",
                "status": "pending_review",
                "detected_at": today,
            }
            new_count += 1
        row = existing[key]
        if row.get("source_active") is False:
            reactivated_count += 1
        row.update({
            "starred": bool(source.get("starred")),
            "forked": bool(source.get("forked")),
            "source_entries": source.get("source_entries", []),
            "source_active": True,
            "last_seen": today,
        })
        if source.get("resolution_errors"):
            row["resolution_errors"] = source["resolution_errors"]
        else:
            row.pop("resolution_errors", None)

    discovered_keys = set(discovered)
    for key, row in existing.items():
        if key not in discovered_keys and row.get("source_active") is not False:
            row["source_active"] = False
            row["last_seen"] = today

    rows = sorted(existing.values(), key=lambda r: str(r["repository"]).lower())
    return rows, new_count, reactivated_count


def stable_state(owner: str, mode: str, discovered: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "owner": owner,
        "discovery_mode": mode,
        "repositories": [discovered[k] for k in sorted(discovered)],
    }


def write_json_if_changed(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def fetch_sources(api: GitHubAPI, owner: str, authenticated_owner: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    encoded = urllib.parse.quote(owner)
    if authenticated_owner:
        stars = api.paginate("/user/starred?per_page=100")
        repos = api.paginate("/user/repos?affiliation=owner&visibility=all&per_page=100")
        repos = [r for r in repos if (r.get("owner") or {}).get("login", "").lower() == owner.lower()]
        mode = "authenticated"
    else:
        stars = api.paginate(f"/users/{encoded}/starred?per_page=100")
        repos = api.paginate(f"/users/{encoded}/repos?type=owner&per_page=100")
        mode = "public"
    forks = [r for r in repos if r.get("fork")]
    return stars, forks, mode


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover new toolbox repositories from GitHub Stars and forks")
    parser.add_argument("--owner", default="embaya")
    parser.add_argument("--catalog-dir", type=Path, default=Path("catalog"))
    parser.add_argument("--pending", type=Path, default=Path("inbox/pending.jsonl"))
    parser.add_argument("--state", type=Path, default=Path("state/discovery.json"))
    parser.add_argument("--result", type=Path, help="Optional JSON run result path")
    args = parser.parse_args()

    toolbox_token = os.getenv("TOOLBOX_GITHUB_TOKEN", "").strip()
    fallback_token = os.getenv("GITHUB_TOKEN", "").strip()
    api = GitHubAPI(toolbox_token or fallback_token or None)

    authenticated_owner = False
    if toolbox_token:
        try:
            user = api.get("/user")
            authenticated_owner = str(user.get("login", "")).lower() == args.owner.lower()
            if not authenticated_owner:
                print(f"warning: TOOLBOX_GITHUB_TOKEN belongs to {user.get('login')!r}, not {args.owner!r}; using public discovery", file=sys.stderr)
        except RuntimeError as exc:
            print(f"warning: could not validate TOOLBOX_GITHUB_TOKEN; using public discovery: {exc}", file=sys.stderr)

    stars, forks, mode = fetch_sources(api, args.owner, authenticated_owner)
    discovered = aggregate_sources(stars, forks, lambda repo: resolve_repo(api, repo))
    catalog_repositories = load_catalog(args.catalog_dir)
    current_pending = read_jsonl(args.pending)
    today = utc_date()
    pending, new_count, reactivated_count = merge_pending(current_pending, discovered, catalog_repositories, today)

    write_jsonl(args.pending, pending)
    write_json_if_changed(args.state, stable_state(args.owner, mode, discovered))

    result = {
        "owner": args.owner,
        "mode": mode,
        "starred_entries": len(stars),
        "fork_entries": len(forks),
        "canonical_discovered": len(discovered),
        "catalog_entries": len(catalog_repositories),
        "pending_entries": len(pending),
        "pending_active": sum(1 for row in pending if row.get("source_active", True)),
        "new_pending": new_count,
        "reactivated_pending": reactivated_count,
    }
    if args.result:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
