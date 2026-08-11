# 18 — Team Task Allocation

> How the three team members split work based on AI access and skills.

---

## 1. Allocation Philosophy

- **Member 1 (40%)**: Backend, architecture, DevOps, integration.
- **Member 2 (40%)**: Mobile app, AI/ML, blockchain integration.
- **Member 3 (20%)**: UI support, testing, documentation, datasets, mock scenarios.

Member 1 and Member 2 own all complex, AI-dependent modules. Member 3 supports with manual tasks, QA, and documentation that do not require extensive AI credits.

---

## 2. Sprint-by-Sprint Allocation

### Sprint 1 — Core Infrastructure

| Task | Owner | Effort |
|------|-------|--------|
| Docker Compose dev environment | Member 1 | 3 days |
| FastAPI scaffold + WebSocket handler | Member 1 | 4 days |
| MongoDB/Redis setup + models | Member 1 | 3 days |
| MERN dashboard scaffold + Mapbox | Member 1 | 4 days |
| React Native bare CLI scaffold | Member 2 | 3 days |
| Permissions + navigation | Member 2 | 2 days |
| Hardhat + contract scaffold | Member 2 | 3 days |
| Initial documentation structure | Member 3 | 3 days |
| Logo/assets organization | Member 3 | 1 day |

### Sprint 2 — Client Telemetry & Offline Buffering

| Task | Owner | Effort |
|------|-------|--------|
| 50Hz IMU + 1Hz GPS service | Member 2 | 4 days |
| Window processor + A_mag | Member 2 | 3 days |
| SQLite offline queue + AES encryption | Member 2 | 4 days |
| Autocommit flush job | Member 2 | 3 days |
| Turf.js geo-fencing | Member 2 | 3 days |
| FastAPI offline reconcile endpoint | Member 1 | 2 days |
| Sensor datasets collection | Member 3 | 4 days |
| UI support (screens, icons) | Member 3 | 3 days |

### Sprint 3 — ML Execution & Authority Communication

| Task | Owner | Effort |
|------|-------|--------|
| LSTM Autoencoder training | Member 2 | 5 days |
| ONNX export + validation | Member 2 | 2 days |
| FastAPI inference worker pool | Member 1 | 3 days |
| Anomaly confirmation logic | Member 1 | 2 days |
| Socket.io incident streaming | Member 1 | 3 days |
| Dashboard incident feed + alerts | Member 1 | 3 days |
| SNN-CAD trajectory analysis | Member 2 | 3 days (stretch) |
| Test data labeling | Member 3 | 4 days |
| Integration test planning | Member 3 | 2 days |

### Sprint 4 — Blockchain DID & e-FIR Automation

| Task | Owner | Effort |
|------|-------|--------|
| Identity Resolution Contract | Member 2 | 3 days |
| Mobile DID onboarding + SecureStore | Member 2 | 4 days |
| IPFS vault encryption/upload | Member 2 | 3 days |
| QR code generation + verification | Member 2 | 2 days |
| e-FIR JSON/PDF microservice | Member 1 | 4 days |
| Haversine dispatch router | Member 1 | 2 days |
| Police/hospital API integration | Member 1 | 3 days |
| Smart contract Amoy deployment | Member 2 | 2 days |
| Hardware prototype assembly | Member 3 + Member 1 | 4 days |
| Demo script + mock scenarios | Member 3 | 3 days |

### Post-Sprint — Integration & Demo

| Task | Owner | Effort |
|------|-------|--------|
| End-to-end integration tests | All | 5 days |
| Load testing | Member 1 | 2 days |
| Hardware validation tests | Member 3 | 3 days |
| Documentation finalization | Member 3 | 3 days |
| Pitch deck + demo rehearsal | All | 3 days |

---

## 3. Decision-Making Authority

| Area | Final Decision Maker |
|------|----------------------|
| Architecture & backend | Member 1 |
| Mobile UX & AI/ML | Member 2 |
| Documentation & QA | Member 3 |
| Blockchain security | Member 1 + Member 2 |
| Scope changes | Team consensus |

---

## 4. Collaboration Rules

- Daily 15-minute standup.
- Weekly review against roadmap.
- Member 3 raises blockers immediately if dependent on Member 1/2.
- All code reviewed by at least one other member.
- Pair programming encouraged for cross-module integrations.
