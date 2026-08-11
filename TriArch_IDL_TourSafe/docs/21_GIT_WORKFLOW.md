# 21 — Git Workflow

> How the team uses Git to collaborate safely.

---

## 1. Branch Strategy

We use a simplified GitHub Flow:

- `main` — production-ready code.
- `develop` — integration branch (optional; can merge directly to `main` for small teams).
- `feature/*` — new features.
- `bugfix/*` — bug fixes.
- `hotfix/*` — urgent production fixes.
- `docs/*` — documentation updates.

---

## 2. Branch Naming

```
feature/mobile-offline-queue
bugfix/backend-websocket-reconnect
docs/update-api-contract
hotfix/dashboard-auth-bypass
```

---

## 3. Commit Message Convention

Use conventional commits:

```
<type>(<scope>): <short description>

<body>
```

Types:
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation only
- `style` — formatting, no logic change
- `refactor` — code restructuring
- `test` — adding or updating tests
- `chore` — build/config/tooling

Examples:
```
feat(mobile): add SQLite offline queue with AES encryption
fix(backend): correct anomaly threshold comparison
 docs: update master context for sprint 2 completion
test(ml): add crash simulation dataset tests
```

---

## 4. Pull Request Process

1. Create feature branch from `main`.
2. Make focused, atomic commits.
3. Push branch to GitHub.
4. Open PR with template filled.
5. Ensure CI passes.
6. Request review from at least one teammate.
7. Address review comments.
8. Squash-merge to `main`.
9. Delete feature branch.

---

## 5. PR Requirements

- [ ] Description explains what and why.
- [ ] Linked to issue (if applicable).
- [ ] Tests added/updated.
- [ ] Documentation updated.
- [ ] `25_CURRENT_STATE.md` updated if status changes.
- [ ] CI green.
- [ ] Review approved.

---

## 6. Releases

- Tag releases on `main`: `v0.1.0`, `v0.2.0`, etc.
- Use semantic versioning.
- Create GitHub release notes from PRs since last tag.

---

## 7. Protected Branches

- `main` requires:
  - PR review
  - CI passing
  - Up-to-date with base branch
- Force push to `main` is disabled.

---

## 8. Handling Conflicts

1. Pull latest `main`.
2. Checkout feature branch.
3. `git rebase main`
4. Resolve conflicts carefully.
5. Force push with lease: `git push --force-with-lease`.

---

## 9. Secrets Policy

- Never commit `.env`, private keys, API keys, or mnemonic phrases.
- Add sensitive files to `.gitignore`.
- Use secret managers in production.
- If a secret is accidentally committed, rotate it immediately.
