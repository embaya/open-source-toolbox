# AI Context — Open Source Toolbox

## What this repository is

This repository is the user's personal registry of open-source tools, frameworks, applications, libraries, agents, workflows and reference implementations that may be reused in personal projects.

Treat the catalog as an **available engineering arsenal**, not as a reading list.

## Required behavior

Whenever the user asks you to design, build, automate, architect or evaluate a project:

1. **Search this toolbox first.** Inspect the relevant JSONL files under `catalog/` and the curated files before recommending that a capability be built from scratch.
2. Identify candidates that match the requested capabilities, not merely keyword similarity.
3. Classify each serious candidate as one of: **DEPLOY**, **INTEGRATE**, **EXTEND**, **INSPIRE**, or **LEARN**.
4. Compare overlapping candidates and recommend the smallest useful set.
5. Consider capability fit, maturity, recent activity, license, self-hosting, API/integration model, operational complexity, security, extensibility and lock-in.
6. Prefer composition of proven components when it reduces risk or time-to-value.
7. Recommend building from scratch only where the toolbox lacks an adequate component or where integration cost exceeds implementation value.
8. External projects not in this catalog may be recommended when materially better; clearly distinguish them from toolbox entries.

## Priority semantics

- **A** — strategic/high-value; inspect first.
- **B** — useful reusable component or strong reference.
- **C** — niche, legacy, educational or situational.

Priority is a navigation aid, not proof of production readiness.

## How to query the catalog

The canonical source is the set of `catalog/*.jsonl` files. Each non-empty line is one JSON object and typically contains repository, URL, category/subcategory, resource type, intended use mode, priority, relevance, description and tags.

For local search:

```bash
python scripts/query_catalog.py --query "multi agent memory observability" --priority A B
```

Start with `TOP_PICKS.md` for high-value candidates and `STACKS.md` for known combinations, then search the full catalog for recall.

## Response pattern when using this toolbox

For architecture/design requests, provide a compact decision table:

| Need | Toolbox candidate | Action | Why | Risks / checks |
|---|---|---|---|---|

Then propose the target architecture and explicitly mark components as **TOOLBOX**, **EXTERNAL**, or **CUSTOM**.

## Safety

Some entries relate to offensive security. Never assume authorization. Restrict security-tool guidance to legitimate, authorized defensive or testing contexts.
