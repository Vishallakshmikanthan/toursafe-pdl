# 19 — Implementation Roadmap

> Timeline from documentation to MVP demo.

---

## 1. Phase 0 — Documentation & Setup (Week 1)

| Week | Tasks | Deliverables |
|------|-------|--------------|
| 1 | Finalize all context docs; create repo structure; set up Docker Compose; initialize project skeletons | Docs v1.0, running dev stack skeleton |

---

## 2. Phase 1 — Sprint 1: Core Infrastructure (Weeks 2–3)

| Week | Focus |
|------|-------|
| 2 | Docker environment; FastAPI backbone; Redis + MongoDB; WebSocket scaffold |
| 3 | MERN dashboard scaffold; Mapbox canvas; React Native skeleton; permissions |

**Deliverables**
- Backend runs and accepts test WebSocket connections.
- Dashboard displays a map.
- Mobile app launches and requests permissions.

---

## 3. Phase 2 — Sprint 2: Client Telemetry & Offline Buffering (Weeks 4–5)

| Week | Focus |
|------|-------|
| 4 | 50Hz IMU + 1Hz GPS; A_mag + sliding window; Turf.js geo-fencing |
| 5 | SQLite queue; AES-256 encryption; autocommit flush; offline reconcile endpoint |

**Deliverables**
- Mobile streams telemetry to backend.
- Geo-fence alerts work offline.
- Offline queue flushes on reconnect.

---

## 4. Phase 3 — Sprint 3: ML Execution & Authority Communication (Weeks 6–7)

| Week | Focus |
|------|-------|
| 6 | LSTM training; threshold calibration; ONNX export |
| 7 | ONNX inference worker; anomaly confirmation; Socket.io streaming; dashboard incident feed |

**Deliverables**
- Model detects simulated crash and immobility.
- Dashboard receives real-time incident alerts.

---

## 5. Phase 4 — Sprint 4: Blockchain DID & e-FIR Automation (Weeks 8–9)

| Week | Focus |
|------|-------|
| 8 | Solidity contract; mobile DID onboarding; IPFS vault; QR code |
| 9 | e-FIR engine; Haversine dispatch; police/hospital API integration; Amoy deployment |

**Deliverables**
- DID registered and resolved on testnet.
- e-FIR auto-generated and dispatched.
- QR scan displays decrypted medical data.

---

## 6. Phase 5 — Integration & Testing (Week 10)

| Week | Focus |
|------|-------|
| 10 | End-to-end integration tests; load tests; hardware validation; bug fixes |

**Deliverables**
- All integration tests passing.
- Load test acceptance met.
- Hardware prototype validated.

---

## 7. Phase 6 — Demo Preparation (Week 11)

| Week | Focus |
|------|-------|
| 11 | Demo scenarios; pitch deck; rehearsal; documentation polish |

**Deliverables**
- Working demo of crash + offline + QR scenarios.
- Pitch deck.
- Final documentation.

---

## 8. Post-MVP Roadmap

| Phase | Timeline | Features |
|-------|----------|----------|
| Phase 2 | Months 4–6 | Bluetooth mesh peer relay, satellite backup, wearables, CV verification, NLP translation |
| Phase 3 | Months 7–12 | Global Safe Zone certification, insurance API integration, cross-border protocol standardization |

---

## 9. Milestone Checklist

- [ ] Week 1: Documentation + repo setup complete.
- [ ] Week 3: Infrastructure sprint complete.
- [ ] Week 5: Telemetry + offline buffering complete.
- [ ] Week 7: ML + real-time dashboard complete.
- [ ] Week 9: Blockchain + e-FIR complete.
- [ ] Week 10: Integration + testing complete.
- [ ] Week 11: Demo ready.
