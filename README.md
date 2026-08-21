# Open Source Toolbox

Personal, AI-ready catalog of reusable open-source projects selected for personal software, AI, automation, infrastructure and content projects.

## Purpose

This repository is a **toolbox, not a bookmark dump**. Before building a component from scratch, use this catalog to identify reusable open-source software that can be deployed, integrated, extended, studied or used as architectural inspiration.

## Catalog status

- **325** classified repositories
- **35** priority A repositories
- **184** priority B repositories
- **36** curated Top Picks
- **7** reusable project stacks

## Start here

| File | Use |
|---|---|
| [`AI_CONTEXT.md`](AI_CONTEXT.md) | Give this to any AI first so it understands how to use the toolbox |
| [`TOOLBOX_PROMPT.md`](TOOLBOX_PROMPT.md) | Copy/paste prompt for ChatGPT, Claude, Gemini, Codex or another AI |
| [`catalog/`](catalog/) | Canonical machine-readable curated catalog, split by functional domain |
| [`metadata/`](metadata/) | Generated GitHub activity, maintenance and maturity overlay |
| [`inbox/`](inbox/) | Newly discovered Stars/forks awaiting curation |
| [`TOP_PICKS.md`](TOP_PICKS.md) | Highest-value tools to inspect first |
| [`STACKS.md`](STACKS.md) | Recommended combinations for common project types |
| [`TAXONOMY.md`](TAXONOMY.md) | Categories, priority and usage semantics |
| [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) | Automatic Stars/forks synchronization |
| [`docs/METADATA.md`](docs/METADATA.md) | Weekly live GitHub metadata refresh |
| [`AGENTS.md`](AGENTS.md) | Instructions for coding agents operating inside this repository |
| [`ROADMAP.md`](ROADMAP.md) | Planned scoring, RAG and MCP evolution |

## Search locally

```bash
python scripts/query_catalog.py --query "multi agent memory observability" --priority A B
python scripts/query_catalog.py --query "kubernetes finops" --limit 10
python scripts/query_catalog.py --category "Automation" --limit 20
python scripts/query_catalog.py --query "agent orchestration" --maintenance ACTIVE SLOW --min-activity 50 --min-maturity 60
```

The last query uses the generated `metadata/github.jsonl` overlay when available. Curated priority and generated activity/maturity signals remain separate.

## Decision workflow

```text
Project requirement
       |
       v
Search catalog/*.jsonl + metadata overlay
       |
       v
Shortlist matching capabilities
       |
       v
DEPLOY / INTEGRATE / EXTEND / INSPIRE / LEARN
       |
       v
Compare maturity, license, maintenance, security and complexity
       |
       v
Choose 1-3 components and compose the architecture
```

## Categories

- **Backend PHP & Symfony** — 57
- **DevOps, Cloud & Infrastructure** — 52
- **IA — Coding Agents & Skills** — 41
- **IA — LLM, RAG & Multimodal** — 34
- **IA — Agents & Multi-agents** — 23
- **Learning & Références** — 21
- **Création média & Vidéo** — 21
- **Automation & Productivité** — 19
- **Frontend, Design & Desktop** — 16
- **Applications Self-hosted & SaaS** — 14
- **Sécurité & Privacy** — 11
- **API, Scraping & Data Acquisition** — 10
- **Finance, Trading & Quant** — 4
- **IoT, Home & Hardware** — 2

## Maintenance model

Your normal collection behavior is the source signal: **Star or fork an interesting repository**. A daily workflow detects new candidates and proposes them in `inbox/pending.jsonl` through a review PR. It never promotes them into the curated catalog automatically.

A separate weekly workflow refreshes GitHub metadata under `metadata/` and proposes changed activity/status signals through another review PR.

## Important

A repository being present here does **not** mean it is production-approved. Before adoption, verify current maintenance activity, license, security posture, deployment model, API stability and fit for the specific project.

Generated `activity_score` and `maturity_score` values are navigation heuristics only; they are not security reviews or production-readiness certifications.

Some security repositories are offensive-security tools. Use them only on systems and targets for which you have explicit authorization.

## Validation

```bash
python -m unittest discover -s tests -p 'test_*.py'
python scripts/validate_catalog.py
python scripts/validate_inbox.py
python scripts/validate_metadata.py
```

Update curated views (`TOP_PICKS.md`, `STACKS.md`) only when a project has been reviewed.
