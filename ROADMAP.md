# Roadmap

## Phase 1 — Portable toolbox (implemented)

- Canonical JSONL catalog
- AI context and universal prompts
- Curated top picks and category views
- Recommended stacks
- Local search CLI
- Catalog validation CI

## Phase 2 — Automated discovery (implemented)

- Daily synchronization of GitHub Stars + owned forks
- Canonical upstream deduplication
- Review inbox for newly discovered projects
- Reusable automation PR instead of direct catalog writes
- Optional authenticated user token with public fallback
- Source-removal tracking without deleting curated knowledge

## Phase 3 — Live GitHub enrichment (implemented foundation)

- license / SPDX
- archived / disabled status
- last push and update dates
- stars / forks / open issues
- latest release metadata
- primary language and topics
- weekly automated refresh PR
- ACTIVE / SLOW / STALE / DORMANT status
- heuristic activity and maturity scores
- metadata-aware local search filters

Still to enrich from repository contents rather than GitHub metadata alone:

- Docker support
- Kubernetes / Helm support
- API / CLI / SDK / MCP support
- self-hosted / SaaS / local-first classification
- documentation quality
- security notes

## Phase 4 — Decision-quality scoring

Potential explicit reviewed scores for:

- integration effort
- operational complexity
- extensibility
- documentation quality
- production readiness
- personal strategic relevance

These should combine automation with reviewed evidence rather than deriving production readiness from GitHub popularity.

## Phase 5 — Retrieval layer

Possible upgrades:

- semantic embeddings over descriptions/README summaries
- lightweight RAG endpoint
- MCP server exposing `search_toolbox`, `get_project`, and `recommend_stack`
- change alerts for archived, renamed or inactive priority-A repositories
