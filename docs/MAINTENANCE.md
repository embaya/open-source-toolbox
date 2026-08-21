# Toolbox maintenance

## Source of discovery

Your normal GitHub behavior remains the input mechanism:

1. Star a repository you want to remember, and/or
2. Fork a repository you consider important enough to keep under your account.

The daily `Discover new repositories` workflow converts these signals into a review inbox.

## Safety boundary

The automation intentionally does **not** modify the curated `catalog/*.jsonl` files. A Star means "interesting", not "production-ready" and not automatically priority A/B/C.

## Public vs authenticated discovery

By default the workflow uses public GitHub endpoints, authenticated with the repository `GITHUB_TOKEN` for rate limiting. This covers public Stars and public owned forks.

For the most complete user-level discovery, create a fine-grained personal access token for the `embaya` account and save it as the repository Actions secret:

`TOOLBOX_GITHUB_TOKEN`

Give it only the minimum read permissions needed for Stars and repository metadata. The script verifies that the token belongs to the configured owner before using `/user/*` endpoints; otherwise it falls back to public discovery.

## Automated PR behavior

The workflow maintains a reusable branch:

`automation/toolbox-discovery`

If a review PR already exists, subsequent runs update the same branch/PR instead of creating duplicates.

If GitHub Actions is not allowed to create pull requests in repository settings, enable **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. The workflow itself requests only `contents: write` and `pull-requests: write`.

## Removing a Star or fork

Removing the source signal does not delete curated knowledge. Pending entries are marked `source_active: false`; curated catalog entries are untouched.
