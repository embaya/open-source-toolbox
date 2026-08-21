# AI Context — Open Source Toolbox

## What this repository is

This repository is the user's personal registry of open-source tools, frameworks, applications, libraries, agents, workflows and reference implementations that may be reused in personal projects.

Treat the catalog as an **available engineering arsenal**, not as a reading list.

## Required behavior

Whenever the user asks you to design, build, automate, architect or evaluate a project:

1. **Search this toolbox first.** Inspect `catalog.jsonl` and relevant curated files before recommending that a capability be built from scratch.
2. Identify candidates that match the requested capabilities, not merely keyword similarity.
3. Classify each serious candidate as one of:
   - **DEPLOY** — use the project substantially as-is.
   - **INTEGRATE** — embed it as a component/library/service.
   - **EXTEND** — fork or adapt it to the project.
   - **INSPIRE** — reuse architecture, patterns, prompts, workflows or implementation ideas.
   - **LEARN** — reference material rather than a runtime dependency.
4. Compare overlapping candidates and recommend the smallest useful set.
5. Consider at least: capability fit, maturity, recent activity, license, self-hosting, API/integration model, operational complexity, security, extensibility and lock-in.
6. Prefer composition of proven components when it reduces risk or time-to-value.
7. Recommend building from scratch only where the toolbox lacks an adequate component or where integration cost exceeds implementation value.
8. External projects not in this catalog may be recommended when they are materially better; clearly distinguish them from toolbox entries.

## Priority semantics

- **A** — strategic/high-value; inspect first.
- **B** — useful reusable component or strong reference.
- **C** — niche, legacy, educational or situational.

Priority is a navigation aid, not proof of production readiness.

## How to query the catalog

The canonical source is `catalog.jsonl`. Each line is one JSON object and typically contains:

- repository
- category / subcategory
- resource_type
- use_mode
- priority
- relevance
- description
- tags

Start with `TOP_PICKS.md` for high-value candidates and `STACKS.md` for known combinations, then use the full catalog for recall.

## Response pattern when using this toolbox

For architecture/design requests, provide a compact decision table:

| Need | Toolbox candidate | Action | Why | Risks / checks |
|---|---|---|---|---|

Then propose the target architecture and explicitly mark components as **Toolbox** vs **External** vs **Custom Build**.

## Safety

Some entries relate to offensive security. Never assume authorization. Restrict security-tool guidance to legitimate, authorized defensive or testing contexts.
