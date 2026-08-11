# 01 — Product Requirements Document (PRD)

> Defines what TourSafe must do, for whom, and how success is measured.

---

## 1. Purpose

TourSafe is a proactive travel safety platform. This document translates the master context into concrete, testable product requirements.

---

## 2. Target Users

| Persona | Needs | Pain Points Addressed |
|---------|-------|----------------------|
| **Solo Adventure Traveler** | Silent protection in remote areas | No one knows if they crash or faint |
| **International Tourist** | Instant identity/medical access abroad | Language barriers, unknown ID, inaccessible medical history |
| **Tour Operator** | Certified safety for customers | Liability, reputation, lack of real-time visibility |
| **Police / EMS Dispatcher** | Automated, structured incident reports | Manual phone calls, paperwork, slow verification |
| **Hospital Emergency Staff** | Blood type, allergies, contacts instantly | Treating unconscious patients with no history |
| **Government Tourism Dept** | Aggregate safety intelligence | No data on high-risk zones or incident patterns |

---

## 3. Functional Requirements

### 3.1 Mobile Application

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| M-01 | App must run on Android 10+ and iOS 14+. | Must | Planned |
| M-02 | App must register traveler, capture medical data, and create DID during onboarding. | Must | Planned |
| M-03 | App must poll accelerometer at target 50Hz in foreground and background. | Must | Planned |
| M-04 | App must poll GPS at 1Hz in background. | Must | Planned |
| M-05 | App must compute A_mag magnitude in real time. | Must | Planned |
| M-06 | App must build 150-point windows with 50% overlap every 1.5s. | Must | Planned |
| M-07 | App must transmit windows to backend via WebSocket when online. | Must | Planned |
| M-08 | App must queue encrypted telemetry in SQLite when offline. | Must | Planned |
| M-09 | App must flush offline queue automatically on reconnect. | Must | Planned |
| M-10 | App must evaluate geo-fences client-side using cached GeoJSON. | Must | Planned |
| M-11 | App must display local alerts for geo-fence entry and confirmed anomalies. | Must | Planned |
| M-12 | App must provide manual SOS override. | Must | Planned |
| M-13 | App must display dynamic QR code for responder identity access. | Must | Planned |
| M-14 | App must show live safety status, connection state, and queue length. | Should | Planned |
| M-15 | App must support adaptive sensor polling to preserve battery. | Should | Planned |

### 3.2 AI / ML Engine

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| AI-01 | Model must be trained only on normal activity data. | Must | Planned |
| AI-02 | Model must accept 150-point A_mag windows. | Must | Planned |
| AI-03 | Model must produce reconstruction error per window. | Must | Planned |
| AI-04 | Anomaly threshold must be calibrated to 99.5th percentile on validation set. | Must | Planned |
| AI-05 | Two consecutive windows must exceed threshold to confirm anomaly. | Must | Planned |
| AI-06 | Model must detect crash/impact signatures. | Must | Planned |
| AI-07 | Model must detect immobility/unconsciousness signatures. | Must | Planned |
| AI-08 | ONNX inference latency must be < 100 ms per window. | Must | Planned |
| AI-09 | SNN-CAD must flag trajectory deviations from safe routes. | Should | Conceptual |
| AI-10 | Model must support periodic retraining with production feedback. | Should | Planned |

### 3.3 Blockchain / DID

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| BC-01 | Each traveler must have one unique W3C DID. | Must | Planned |
| BC-02 | Private key must be generated and stored on device only. | Must | Planned |
| BC-03 | Smart contract must register DID with public key hash and IPFS CID. | Must | Planned |
| BC-04 | Smart contract must resolve DID to public key + IPFS CID. | Must | Planned |
| BC-05 | Emergency access must only be granted after AI-confirmed anomaly. | Must | Planned |
| BC-06 | Access grants must be time-limited and revocable. | Must | Planned |
| BC-07 | Every access grant must emit an immutable on-chain event. | Must | Planned |
| BC-08 | Responder must decrypt medical vault within 15 seconds of QR scan. | Must | Planned |
| BC-09 | Contract must deploy on Polygon Amoy for testing and mainnet for production. | Must | Planned |

### 3.4 Backend

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| B-01 | Backend must accept persistent WebSocket connections from mobile devices. | Must | Planned |
| B-02 | Backend must cache latest GPS in Redis with 5-minute TTL. | Must | Planned |
| B-03 | Backend must archive telemetry and incidents in MongoDB. | Must | Planned |
| B-04 | Backend must emit confirmed anomalies to dashboard via Socket.io. | Must | Planned |
| B-05 | Backend must handle 1,000 concurrent telemetry streams. | Must | Planned |
| B-06 | Backend must expose REST APIs for dashboard queries. | Must | Planned |
| B-07 | Backend must support offline-queue reconciliation. | Must | Planned |

### 3.5 Dashboard

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| D-01 | Dashboard must display live traveler positions on Mapbox map. | Must | Planned |
| D-02 | Dashboard must color-code travelers by safety status. | Must | Planned |
| D-03 | Dashboard must show real-time incident feed. | Must | Planned |
| D-04 | Dashboard must render geo-fence boundaries. | Must | Planned |
| D-05 | Dashboard must show incident heatmaps. | Should | Planned |
| D-06 | Dashboard must support agency login with JWT. | Must | Planned |
| D-07 | Dashboard must allow operator confirmation before full e-FIR dispatch. | Must | Planned |
| D-08 | Dashboard must display decrypted medical data after QR scan. | Must | Planned |

### 3.6 e-FIR Engine

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| E-01 | e-FIR must auto-generate upon confirmed anomaly. | Must | Planned |
| E-02 | e-FIR must include incident ID, timestamp, victim identity, GPS, anomaly type, LSTM error trace. | Must | Planned |
| E-03 | e-FIR must include decrypted blood type, allergies, conditions, contacts. | Must | Planned |
| E-04 | e-FIR must be produced as JSON and PDF. | Must | Planned |
| E-05 | e-FIR must dispatch to nearest police and hospital nodes. | Must | Planned |
| E-06 | e-FIR dispatch latency must be < 60 seconds. | Must | Planned |

### 3.7 Hardware Prototype

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| H-01 | Prototype must poll MPU6050 IMU at 50Hz. | Must | Planned |
| H-02 | Prototype must read NEO-6M GPS coordinates. | Must | Planned |
| H-03 | Prototype must transmit telemetry to backend. | Must | Planned |
| H-04 | Prototype must trigger anomaly LED/buzzer on high-G event. | Should | Planned |
| H-05 | Prototype must demonstrate offline buffering. | Should | Planned |

---

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NF-01 | Mean time to respond (AI confirm → responder ack) | < 5 min |
| NF-02 | e-FIR dispatch latency | < 60 s |
| NF-03 | DID resolution latency (QR scan → data display) | < 15 s |
| NF-04 | LSTM inference latency | < 100 ms |
| NF-05 | 99th percentile telemetry→dashboard latency at peak load | < 500 ms |
| NF-06 | Offline data recovery rate | > 99.9% |
| NF-07 | False positive rate after two-stage confirmation | < 2% |
| NF-08 | Concurrent telemetry streams supported | 1,000+ |
| NF-09 | Battery impact | Acceptable for 8-hour trip |
| NF-10 | Uptime (production) | 99.9% |

---

## 5. Success Metrics (KPIs)

| KPI | Definition | Target |
|-----|------------|--------|
| MTTR | AI confirm to first responder acknowledgment | < 5 min |
| False Positive Rate | Anomaly flags without real emergency | < 2% |
| Active Monitoring Coverage | Simultaneously tracked travelers | 5,000+ |
| Offline Data Recovery Rate | Queued telemetry successfully flushed | > 99.9% |
| DID Resolution Latency | QR scan to decrypted data display | < 15 s |
| e-FIR Dispatch Latency | AI confirm to police/hospital receipt | < 60 s |

---

## 6. Constraints & Assumptions

- Travelers grant explicit consent during onboarding.
- Target devices have accelerometer, GPS, and internet (intermittent acceptable).
- Police/hospital nodes expose REST endpoints to receive e-FIR payloads.
- Government agencies undergo onboarding to receive Emergency Cryptographic Access Keys.
- Polygon network is available for DID operations.

---

## 7. Out of Scope

- Direct-to-consumer payment/subscription in MVP.
- Real-time video streaming.
- Drone or robotic dispatch.
- Wearable integration.
- Satellite connectivity.

---

## 8. Approval

| Role | Name | Sign-off |
|------|------|----------|
| Product Owner | Vishal Lakshmikanthan | Pending |
| Tech Lead | Member 1 | Pending |
| ML Lead | Member 2 | Pending |
| QA / Docs | Member 3 | Pending |
