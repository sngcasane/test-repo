# Contributing to Acme Corp

This document is the source of truth for how we work. Read it once on your
first day and refer back when you're unsure.

## Branch naming

We use a strict naming convention so branches sort sensibly:

- `feature/<ticket-id>-short-description` — new functionality
- `bugfix/<ticket-id>-short-description` — bug fixes
- `hotfix/<ticket-id>-short-description` — urgent production fixes
- `chore/<short-description>` — refactors, dependency bumps, tooling

Example: `feature/PAY-1284-add-refund-endpoint`

## Commit messages

Conventional Commits format. The first line is `<type>: <description>` and
must be under 72 characters. Types we use: `feat`, `fix`, `chore`, `docs`,
`refactor`, `test`, `perf`.

Example: `feat: add refund endpoint to payments service`

## Pull request process

1. Open the PR against `main`. We don't use long-lived feature branches.
2. Fill in the PR template — what changed, why, how it was tested.
3. Request review from at least one engineer. PRs touching the payments
   service additionally require review from a Senior Engineer.
4. Address all review comments. Resolve threads as you go.
5. Squash and merge once approved. We do NOT use merge commits.

## Code review checklist

Reviewers should confirm:

- [ ] Tests cover the change. New code is typed end-to-end.
- [ ] Logs use structured logging (no `print` outside scripts).
- [ ] No secrets, API keys, or PII in the diff.
- [ ] Public functions have docstrings.
- [ ] Breaking API changes are flagged in the PR description.
- [ ] Database migrations are reversible (down() implemented).

## When NOT to merge

- During the production freeze window (Friday 14:00 UTC → Monday 09:00 UTC),
  only hotfixes are merged.
- If CI is red. Fix CI before merging.
- If you haven't tested your change against a real database — `pytest` alone
  is not sufficient for changes touching the data layer.
