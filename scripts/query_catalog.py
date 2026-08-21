#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "catalog.jsonl"

def load():
    with CATALOG.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

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
        if isinstance(value, list): value = " ".join(value)
        hay = (value or "").lower()
        for token in query_tokens:
            if token in hay: total += weight
    total += {"A": 3, "B": 1}.get(repo.get("priority"), 0)
    total += max(0, (repo.get("relevance") or 0) - 3)
    return total

def main():
    p=argparse.ArgumentParser(description="Search the Open Source Toolbox catalog")
    p.add_argument("--query", "-q", default="", help="Free-text capability search")
    p.add_argument("--category", help="Exact or partial category filter")
    p.add_argument("--priority", nargs="*", choices=["A","B","C"], help="Allowed priorities")
    p.add_argument("--mode", help="Partial use_mode filter")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--json", action="store_true", help="Output JSON")
    args=p.parse_args()
    rows=load(); q=tokens(args.query)
    result=[]
    for r in rows:
        if args.category and args.category.lower() not in (r.get("category") or "").lower(): continue
        if args.priority and r.get("priority") not in args.priority: continue
        if args.mode and args.mode.lower() not in (r.get("use_mode") or "").lower(): continue
        s=score(r,q) if q else ({"A":3,"B":2,"C":1}.get(r.get("priority"),0)+(r.get("relevance") or 0))
        if q and s <= 0: continue
        result.append((s,r))
    result.sort(key=lambda x:(-x[0], {"A":0,"B":1,"C":2}.get(x[1].get("priority"),9), x[1]["repository"].lower()))
    result=result[:max(1,args.limit)]
    if args.json:
        print(json.dumps([{**r,"_score":s} for s,r in result],ensure_ascii=False,indent=2))
        return
    print(f"{'SCORE':>5}  {'P':1}  {'REPOSITORY':42}  CATEGORY")
    print("-"*110)
    for s,r in result:
        print(f"{s:>5}  {r.get('priority','?'):1}  {r['repository'][:42]:42}  {r.get('category','')}")
        print(f"       {r.get('description','')}")

if __name__ == "__main__":
    main()
