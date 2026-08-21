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
| [`catalog.jsonl`](catalog.jsonl) | Canonical machine-readable catalog, one repository per line |
| [`CATALOG_AI.tsv`](CATALOG_AI.tsv) | Compact tabular catalog for LLMs and spreadsheets |
| [`TOP_PICKS.md`](TOP_PICKS.md) | Highest-value tools to inspect first |
| [`STACKS.md`](STACKS.md) | Recommended combinations for common project types |
| [`TAXONOMY.md`](TAXONOMY.md) | Categories, priority and usage semantics |
| [`AGENTS.md`](AGENTS.md) | Instructions for coding agents operating inside this repository |

## Decision workflow

```text
Project requirement
       |
       v
Search catalog.jsonl
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

## Important

A repository being present here does **not** mean it is production-approved. Before adoption, verify current maintenance activity, license, security posture, deployment model, API stability and fit for the specific project.

Some security repositories are offensive-security tools. Use them only on systems and targets for which you have explicit authorization.

## Updating the toolbox

When new repositories are added, keep `catalog.jsonl` as the canonical machine-readable source and update the curated views only when the project has been reviewed.
