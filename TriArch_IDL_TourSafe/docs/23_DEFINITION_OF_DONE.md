# 23 — Definition of Done

> Criteria that must be met before any TourSafe work item is considered complete.

---

## 1. Universal Done Criteria

For every task, story, or PR:

- [ ] Code implemented according to spec.
- [ ] Code follows project conventions (see `00_MASTER_CONTEXT.md` Section 25).
- [ ] No secrets, keys, or credentials in code.
- [ ] Linter/formatter passes.
- [ ] Unit tests added and passing.
- [ ] PR reviewed and approved by at least one teammate.
- [ ] CI pipeline passes.
- [ ] Relevant documentation updated.
- [ ] `25_CURRENT_STATE.md` updated if feature status changed.
- [ ] `24_CHANGELOG.md` updated.

---

## 2. Module-Specific Criteria

### Mobile Feature Done
- [ ] Works on Android and iOS (or documented limitation).
- [ ] Handles foreground, background, and offline states.
- [ ] Permissions requested and gracefully denied.
- [ ] UI tested on target screen sizes.
- [ ] No memory leaks in sensor listeners.

### Backend Feature Done
- [ ] Async handlers do not block event loop.
- [ ] Pydantic models validate inputs/outputs.
- [ ] Redis/MongoDB operations handle failures.
- [ ] WebSocket reconnect logic tested.
- [ ] Logs are structured and useful.

### ML Feature Done
- [ ] Model training reproducible (seed fixed).
- [ ] Evaluation metrics recorded.
- [ ] ONNX export validated against TF output.
- [ ] Inference latency benchmarked.
- [ ] Dataset documented and versioned.

### Blockchain Feature Done
- [ ] Hardhat tests cover all functions.
- [ ] Gas costs estimated.
- [ ] Events emitted for state changes.
- [ ] Deployed to testnet for integration.
- [ ] No critical Slither findings.

### Dashboard Feature Done
- [ ] Responsive layout.
- [ ] Real-time updates via Socket.io.
- [ ] JWT-protected routes.
- [ ] Error states handled (loading, empty, error).

### Hardware Feature Done
- [ ] Wiring diagram updated.
- [ ] Firmware compiles and uploads.
- [ ] Validation test log signed off.
- [ ] Demo script updated.

---

## 3. Release Done Criteria

Before any release tag:

- [ ] All sprint tasks meet done criteria.
- [ ] Integration tests pass.
- [ ] Load tests meet acceptance.
- [ ] Security scan clean.
- [ ] Documentation complete.
- [ ] Demo scenarios validated.
- [ ] Team sign-off.
