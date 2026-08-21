# Roadmap

## Phase 1 — Portable toolbox (implemented)

- Canonical JSONL catalog
- Compact LLM catalog
- AI context and universal prompts
- Curated top picks and category views
- Recommended stacks
- Local search CLI
- Catalog validation CI

## Phase 2 — Live GitHub enrichment

Add periodically refreshed metadata:

- license / SPDX
- archived / disabled status
- last push date
- stars / forks
- releases / latest release date
- primary language
- Docker support
- Kubernetes / Helm support
- API / CLI / SDK / MCP support
- self-hosted / SaaS / local-first classification
- security notes

## Phase 3 — Decision-quality scoring

Add explicit scores for:

- maturity
- maintenance health
- documentation
- integration effort
- operational complexity
- extensibility
- production readiness
- personal strategic relevance

## Phase 4 — Retrieval layer

Possible upgrades:

- semantic embeddings over descriptions/README summaries
- lightweight RAG endpoint
- MCP server exposing `search_toolbox`, `get_project`, and `recommend_stack`
- automated weekly refresh of metadata
- change alerts for archived, renamed or inactive priority-A repositories
