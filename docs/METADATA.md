# Metadata refresh

The weekly metadata refresh complements the curated toolbox with live GitHub signals while keeping automation and human judgment separate.

## Schedule

The `Refresh GitHub metadata` workflow runs weekly, can be dispatched manually, and also runs when the metadata-refresh implementation is first merged to `master`.

It maintains a reusable branch:

`automation/toolbox-metadata`

Changes are proposed through a draft PR instead of being committed directly to `master`.

## Authentication

The workflow uses the repository `GITHUB_TOKEN` for public GitHub repository metadata. The curated catalog is currently composed of public upstream projects, so a personal token is not required for the normal case.

## What automation may change

Only generated metadata under `metadata/`.

It must not rewrite:

- curated categories
- priority A/B/C
- relevance
- descriptions written during curation
- architectural recommendations in `TOP_PICKS.md` or `STACKS.md`

## Interpreting scores

The scores are designed to help shortlist candidates. Before choosing a component, inspect the upstream repository, current license, security posture, releases, open issues and project-specific fit.
