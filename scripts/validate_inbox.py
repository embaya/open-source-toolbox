#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

PENDING = Path("inbox/pending.jsonl")
ALLOWED_STATUS = {"pending_review", "keep", "archive", "remove"}
errors: list[str] = []
seen: set[str] = set()
count = 0

if PENDING.exists():
    for lineno, line in enumerate(PENDING.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: invalid JSON: {exc}")
            continue
        repo = str(row.get("repository", "")).strip()
        if not repo or "/" not in repo:
            errors.append(f"line {lineno}: invalid repository {repo!r}")
            continue
        key = repo.lower()
        if key in seen:
            errors.append(f"line {lineno}: duplicate repository {repo}")
        seen.add(key)
        if row.get("status") not in ALLOWED_STATUS:
            errors.append(f"line {lineno}: invalid status {row.get('status')!r}")
        for field in ("starred", "forked", "source_active"):
            if field in row and not isinstance(row[field], bool):
                errors.append(f"line {lineno}: {field} must be boolean")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"OK: {count} pending inbox entries")
