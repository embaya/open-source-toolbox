#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'catalog.jsonl'
required={'repository','category','priority','description'}
seen=set(); errors=[]; count=0
for lineno,line in enumerate(CATALOG.read_text(encoding='utf-8').splitlines(),1):
    if not line.strip(): continue
    count+=1
    try: row=json.loads(line)
    except json.JSONDecodeError as e:
        errors.append(f"line {lineno}: invalid JSON: {e}"); continue
    missing=required-set(row)
    if missing: errors.append(f"line {lineno}: missing {sorted(missing)}")
    repo=row.get('repository')
    if repo in seen: errors.append(f"line {lineno}: duplicate repository {repo}")
    seen.add(repo)
    if row.get('priority') not in {'A','B','C'}: errors.append(f"line {lineno}: invalid priority {row.get('priority')}")
    rel=row.get('relevance')
    if rel is not None and not (1 <= rel <= 5): errors.append(f"line {lineno}: invalid relevance {rel}")
if errors:
    print('\n'.join(errors),file=sys.stderr); sys.exit(1)
print(f"OK: {count} unique catalog entries")
