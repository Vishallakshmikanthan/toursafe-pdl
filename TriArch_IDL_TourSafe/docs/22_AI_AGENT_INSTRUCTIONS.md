# 22 — AI Agent Instructions

> Instructions for Claude, ChatGPT, Gemini, Copilot, or any coding agent working on TourSafe.

---

## 1. Mandatory First Step

Before writing, editing, or reviewing any code or documentation, **read `docs/00_MASTER_CONTEXT.md`**.

Then read the relevant domain spec:
- Mobile work → `04_MOBILE_APP_SPECIFICATION.md`
- Backend work → `05_BACKEND_SPECIFICATION.md`
- ML work → `06_AI_ML_SPECIFICATION.md`
- Blockchain work → `07_BLOCKCHAIN_DID_SPECIFICATION.md`
- Geo-fencing → `08_GEOFENCING_SPECIFICATION.md`
- Emergency/e-FIR → `09_EMERGENCY_RESPONSE_ENGINE.md`
- Offline → `10_OFFLINE_FIRST_SPECIFICATION.md`
- API → `12_API_CONTRACT.md`
- WebSocket → `13_WEBSOCKET_CONTRACT.md`
- Security → `14_SECURITY_PRIVACY.md`

---

## 2. Feature Status Rules

Use these exact labels in code comments, docs, and `00_MASTER_CONTEXT.md`:

- `IMPLEMENTED` — code exists and is validated.
- `IN DEVELOPMENT` — actively being built.
- `PLANNED` — scheduled in current roadmap.
- `CONCEPTUAL` — future idea, do not implement yet.

Never mark a feature as `IMPLEMENTED` unless tests pass and a teammate has reviewed it.

---

## 3. Code Style Rules

- **Python**: type hints, Pydantic models, `async/await`, `black`/`isort` formatting.
- **TypeScript**: strict mode, explicit types, functional components, no `any`.
- **Solidity**: explicit access modifiers, events for state changes, OpenZeppelin where helpful.
- **No hardcoded secrets**. Use environment variables.
- **No magic numbers**. Define constants.
- **No deeply nested code**. Prefer early returns.

---

## 4. What to Do Before Committing

1. Run relevant unit tests.
2. Run linter/formatter.
3. Update or add docstrings/comments.
4. Update `docs/25_CURRENT_STATE.md` if a feature status changes.
5. Update `docs/24_CHANGELOG.md` under Unreleased.
6. Ensure no secrets in diff.

---

## 5. What to Avoid

- Do not change architecture without updating `02_SYSTEM_ARCHITECTURE.md`.
- Do not add new dependencies without justification in PR description.
- Do not delete or rename files unless explicitly asked.
- Do not implement conceptual features unless told to prioritize them.
- Do not skip tests for life-critical code (anomaly detection, encryption, dispatch).

---

## 6. How to Ask for Clarification

If context is ambiguous:
1. State your assumption clearly.
2. Ask the user which option to choose.
3. Do not guess on security, privacy, or architecture.

---

## 7. Documentation Updates

Every AI agent must help maintain documentation. If you change behavior, update:
- `00_MASTER_CONTEXT.md` feature inventory and decision log.
- Domain-specific spec file.
- `25_CURRENT_STATE.md`.
- `24_CHANGELOG.md`.

---

## 8. Example Prompt Template for Future AI Use

When asking an AI to implement a TourSafe module, use this template:

```
You are working on TourSafe. Read docs/00_MASTER_CONTEXT.md and the relevant domain spec first.

Task: <specific task>

Constraints:
- Keep within MVP scope.
- Follow existing code style.
- Add/update tests.
- Update docs/25_CURRENT_STATE.md and docs/24_CHANGELOG.md.

Expected output: <files to create/modify>
```
