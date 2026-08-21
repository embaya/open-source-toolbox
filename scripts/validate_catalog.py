#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "catalog"
REQUIRED = {"repository", "category", "priority", "description"}
EXPECTED_COUNT = 325

seen = set()
errors = []
count = 0
files = sorted(CATALOG_DIR.glob("*.jsonl"))

if not files:
    errors.append("no catalog/*.jsonl files found")

for path in files:
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}:{lineno}: invalid JSON: {e}")
            continue
        missing = REQUIRED - set(row)
        if missing:
            errors.append(f"{path.name}:{lineno}: missing {sorted(missing)}")
        repo = row.get("repository")
        if repo in seen:
            errors.append(f"{path.name}:{lineno}: duplicate repository {repo}")
        seen.add(repo)
        if row.get("priority") not in {"A", "B", "C"}:
            errors.append(f"{path.name}:{lineno}: invalid priority {row.get('priority')}")
        rel = row.get("relevance")
        if rel is not None and not (1 <= rel <= 5):
            errors.append(f"{path.name}:{lineno}: invalid relevance {rel}")

if count != EXPECTED_COUNT:
    errors.append(f"expected {EXPECTED_COUNT} entries, found {count}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

print(f"OK: {count} unique catalog entries across {len(files)} files")
