# Review Inbox

`pending.jsonl` contains repositories discovered from GitHub Stars and owned forks that are **not yet present in the curated catalog**.

The discovery workflow may update only source/provenance fields such as:

- `starred`
- `forked`
- `source_entries`
- `source_active`
- `last_seen`
- `resolution_errors`

Human/AI review may add notes while an item is pending. Discovery preserves unknown/manual fields.

## Status values

- `pending_review` — not yet curated.
- `keep` — explicitly retained in the inbox for later analysis.
- `archive` — no longer active but intentionally remembered.
- `remove` — explicitly marked for removal from the inbox.

A repository must **not** enter `catalog/*.jsonl` solely because it was starred or forked. Classification and architectural relevance remain curated decisions.
