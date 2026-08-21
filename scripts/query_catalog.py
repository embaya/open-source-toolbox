#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "catalog"
METADATA_FILE = ROOT / "metadata" / "github.jsonl"


def load_jsonl(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load():
    rows = []
    for path in sorted(CATALOG_DIR.glob("*.jsonl")):
        rows.extend(load_jsonl(path))
    metadata = {r["repository"].lower(): r for r in load_jsonl(METADATA_FILE) if r.get("repository")}
    return [(row, metadata.get(row["repository"].lower(), {})) for row in rows]


def tokens(text):
    return [t for t in re.findall(r"[\w+#.-]+", (text or "").lower()) if len(t) > 1]


def score(repo, query_tokens):
    fields = {
        "repository": 5,
        "category": 4,
        "subcategory": 4,
        "resource_type": 3,
        "description": 3,
        "tags": 4,
    }
    total = 0
    for field, weight in fields.items():
        value = repo.get(field)
        if isinstance(value, list):
            value = " ".join(value)
        hay = (value or "").lower()
        for token in query_tokens:
            if token in hay:
                total += weight
    total += {"A": 3, "B": 1}.get(repo.get("priority"), 0)
    total += max(0, (repo.get("relevance") or 0) - 3)
    return total


def main():
    p = argparse.ArgumentParser(description="Search the Open Source Toolbox catalog")
    p.add_argument("--query", "-q", default="", help="Free-text capability search")
    p.add_argument("--category", help="Exact or partial category filter")
    p.add_argument("--priority", nargs="*", choices=["A", "B", "C"], help="Allowed curated priorities")
    p.add_argument("--mode", help="Partial use_mode filter")
    p.add_argument("--maintenance", nargs="*", choices=["ACTIVE", "SLOW", "STALE", "DORMANT", "ARCHIVED", "DISABLED", "MISSING", "INACCESSIBLE", "UNKNOWN"], help="Allowed GitHub maintenance states")
    p.add_argument("--min-activity", type=int, default=0, help="Minimum generated activity score (0-100)")
    p.add_argument("--min-maturity", type=int, default=0, help="Minimum generated maturity score (0-100)")
    p.add_argument("--language", help="GitHub primary language filter")
    p.add_argument("--license", dest="license_filter", help="GitHub SPDX/license filter")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--json", action="store_true", help="Output JSON including GitHub metadata overlay")
    args = p.parse_args()

    q = tokens(args.query)
    result = []
    for r, m in load():
        if args.category and args.category.lower() not in (r.get("category") or "").lower():
            continue
        if args.priority and r.get("priority") not in args.priority:
            continue
        if args.mode and args.mode.lower() not in (r.get("use_mode") or "").lower():
            continue
        if args.maintenance and m.get("maintenance_status") not in args.maintenance:
            continue
        if args.min_activity and (m.get("activity_score") or 0) < args.min_activity:
            continue
        if args.min_maturity and (m.get("maturity_score") or 0) < args.min_maturity:
            continue
        if args.language and args.language.lower() not in (m.get("language") or "").lower():
            continue
        if args.license_filter and args.license_filter.lower() not in (m.get("license") or "").lower():
            continue

        s = score(r, q) if q else ({"A": 3, "B": 2, "C": 1}.get(r.get("priority"), 0) + (r.get("relevance") or 0))
        if q and s <= 0:
            continue
        result.append((s, r, m))

    result.sort(key=lambda x: (
        -x[0],
        {"A": 0, "B": 1, "C": 2}.get(x[1].get("priority"), 9),
        -(x[2].get("activity_score") or 0),
        -(x[2].get("maturity_score") or 0),
        x[1]["repository"].lower(),
    ))
    result = result[:max(1, args.limit)]

    if args.json:
        print(json.dumps([
            {**repo, "_score": s, "github": metadata}
            for s, repo, metadata in result
        ], ensure_ascii=False, indent=2))
        return

    print(f"{'SCORE':>5} {'P':1} {'ACT':>3} {'MAT':>3} {'STATUS':10} {'REPOSITORY':38} CATEGORY")
    print("-" * 130)
    for s, r, m in result:
        print(
            f"{s:>5} {r.get('priority', '?'):1} "
            f"{(m.get('activity_score') if m else '-'):>3} "
            f"{(m.get('maturity_score') if m else '-'):>3} "
            f"{(m.get('maintenance_status') or '-'):10} "
            f"{r['repository'][:38]:38} {r.get('category', '')}"
        )
        print(f"      {r.get('description', '')}")


if __name__ == "__main__":
    main()
