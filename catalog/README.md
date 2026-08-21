# Catalog

The catalog contains **325 unique repositories** in JSON Lines format. Each non-empty line is one JSON object.

The files are split by functional domain so humans and AI assistants can load only the relevant subset. Large domains are split into numbered parts.

## Fields

- `repository` — canonical `owner/name`
- `url` — GitHub URL
- `category` — primary functional domain
- `subcategory` — more precise role
- `resource_type` — framework, application, skill, reference, tool, etc.
- `use_mode` — intended way to reuse it
- `priority` — A / B / C navigation priority
- `relevance` — 1–5 relevance score
- `description` — concise practical description
- `tags` — optional cross-cutting keywords

## Loading the complete catalog

```python
import json
from pathlib import Path

rows = []
for path in sorted(Path("catalog").glob("*.jsonl")):
    with path.open(encoding="utf-8") as f:
        rows.extend(json.loads(line) for line in f if line.strip())

print(len(rows))  # 325
```

For interactive search use:

```bash
python scripts/query_catalog.py --query "multi agent memory observability" --priority A B
python scripts/query_catalog.py --query "kubernetes finops" --limit 10
python scripts/query_catalog.py --category "Automation" --limit 20
```

Run `python scripts/validate_catalog.py` after modifying catalog data.
