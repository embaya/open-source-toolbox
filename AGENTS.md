# AGENTS.md

## Purpose

This repository is an AI-readable open-source component registry.

## Instructions for coding agents

- Read `AI_CONTEXT.md` before architecture recommendations.
- Use all `catalog/*.jsonl` files as the canonical catalog; load only relevant domains when possible.
- Prefer precise filtering over dumping large lists of repositories.
- Use `python scripts/query_catalog.py --query "<capabilities>"` for local retrieval.
- For a concrete project, shortlist 3-8 candidates and then inspect their upstream repositories before final adoption.
- Distinguish `TOOLBOX`, `EXTERNAL`, and `CUSTOM` components in architecture proposals.
- Never infer production readiness solely from priority or GitHub popularity.
- Do not rewrite curated metadata without evidence.
- When refreshing metadata, preserve human curation fields and provenance.
- Treat offensive-security entries as authorized-testing references only.
