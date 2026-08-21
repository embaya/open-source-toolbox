#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_STATUS = {"ACTIVE", "SLOW", "STALE", "DORMANT", "ARCHIVED", "DISABLED", "MISSING", "INACCESSIBLE", "UNKNOWN"}


def read_jsonl(path: Path):
    if not path.exists(): return []
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try: rows.append((lineno, json.loads(line)))
        except json.JSONDecodeError as exc: raise RuntimeError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
    return rows


def catalog_set(catalog_dir: Path) -> set[str]:
    result = set()
    for path in catalog_dir.glob("*.jsonl"):
        for _, row in read_jsonl(path):
            if row.get("repository"): result.add(str(row["repository"]).lower())
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=Path("metadata/github.jsonl"))
    parser.add_argument("--catalog-dir", type=Path, default=Path("catalog"))
    parser.add_argument("--require-coverage", action="store_true")
    args = parser.parse_args()

    errors = []
    seen = set()
    rows = read_jsonl(args.metadata)
    for lineno, row in rows:
        repo = str(row.get("repository", "")).strip()
        if not repo or "/" not in repo:
            errors.append(f"line {lineno}: invalid repository {repo!r}")
            continue
        key = repo.lower()
        if key in seen: errors.append(f"line {lineno}: duplicate repository {repo}")
        seen.add(key)
        if row.get("maintenance_status") not in ALLOWED_STATUS:
            errors.append(f"line {lineno}: invalid maintenance_status {row.get('maintenance_status')!r}")
        for score_name in ("activity_score", "maturity_score"):
            score = row.get(score_name)
            if not isinstance(score, int) or not 0 <= score <= 100:
                errors.append(f"line {lineno}: {score_name} must be integer 0..100")

    catalog = catalog_set(args.catalog_dir)
    extras = seen - catalog
    if extras: errors.append(f"metadata contains {len(extras)} repositories not present in catalog")
    if args.require_coverage:
        missing = catalog - seen
        if missing: errors.append(f"metadata missing {len(missing)} catalog repositories")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {len(rows)} metadata rows; catalog={len(catalog)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
