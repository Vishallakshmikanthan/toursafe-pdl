# 17 — Demo Scenarios

> Scripted scenarios to demonstrate TourSafe capabilities in presentations, reviews, and pitches.

---

## 1. Scenario A: Crash Detection & e-FIR Dispatch

### Goal
Show autonomous crash detection, identity resolution, and e-FIR dispatch.

### Steps
1. Traveler starts a trip in the mobile app.
2. Mobile streams normal telemetry (walking/driving).
3. Operator shows live map in dashboard; traveler dot is green.
4. Simulate crash: drop hardware prototype or inject high-G window.
5. LSTM reconstruction error spikes.
6. Two consecutive windows exceed threshold → confirmed CRASH.
7. Dashboard shows red alert with GPS, traveler profile.
8. Blockchain access grant transaction is submitted.
9. e-FIR JSON/PDF generated and "dispatched" to mock police/hospital APIs.
10. Responder scans traveler QR code.
11. Decrypted medical data (blood type, allergies, contacts) displayed.

### Talking Points
- "No button was pressed. The AI detected the crash from motion alone."
- "Identity and medical data arrived in seconds, not minutes."

---

## 2. Scenario B: Immobility in Remote Zone

### Goal
Demonstrate unconsciousness/immobility detection.

### Steps
1. Traveler enters a remote hazard zone.
2. Geo-fence breach triggers amber alert.
3. Traveler becomes immobile; phone flatlines at ~9.81 m/s².
4. GPS remains static in remote area.
5. After dwell threshold, system confirms IMMOBILITY alert.
6. e-FIR dispatched; responder decrypts vault.

### Talking Points
- "The system protects travelers who cannot reach their phone."
- "Remote location does not mean invisible."

---

## 3. Scenario C: Offline Resilience

### Goal
Show offline buffering and automatic sync.

### Steps
1. Traveler enters no-signal zone.
2. Mobile continues recording; telemetry encrypts into SQLite queue.
3. App shows "Offline — data safely queued" indicator.
4. Traveler re-enters coverage.
5. Autocommit flushes queued windows in chronological order.
6. Dashboard retroactively reconstructs path and detects any anomaly.

### Talking Points
- "No data was lost, even without connectivity."
- "The queue preserves the timeline for post-incident analysis."

---

## 4. Scenario D: Manual SOS Override

### Goal
Show conscious traveler-initiated emergency.

### Steps
1. Traveler feels unsafe or witnesses another emergency.
2. Opens app and presses SOS.
3. Countdown allows cancellation.
4. After countdown, SOS event sent.
5. Dashboard receives CRITICAL alert immediately.
6. e-FIR generated and dispatched.

---

## 5. Scenario E: Authority Dashboard Operations

### Goal
Show the B2G operational interface.

### Steps
1. Agency operator logs into dashboard.
2. Live map shows all travelers in jurisdiction.
3. Heatmap overlay shows historical incident hotspots.
4. Geo-fence boundaries displayed.
5. Operator clicks incident card to view details.
6. Operator confirms incident and dispatches e-FIR.
7. Operator marks incident resolved.

---

## 6. Demo Data Sets

| File | Purpose |
|------|---------|
| `tests/data/demo_normal_walk.csv` | 5 min normal walking |
| `tests/data/demo_crash_impulse.csv` | High-G crash window |
| `tests/data/demo_immobile.csv` | Stationary flatline |
| `tests/data/demo_geo_fence.json` | Test hazard polygon |
| `tests/data/demo_medical_profile.json` | Sample vault content |

---

## 7. Demo Environment

- Local Docker Compose stack.
- Hardhat local node for instant blockchain transactions.
- Mock police/hospital endpoints.
- One Android emulator + one hardware prototype.
- Pre-loaded demo accounts and geo-fences.

---

## 8. Presentation Narrative

1. **Problem**: Show news clip or statistic about tourist emergency delays.
2. **Solution overview**: Three-layer shield.
3. **Live demo A**: Crash detection.
4. **Live demo B**: Offline resilience.
5. **Dashboard walkthrough**: Real-time operations.
6. **Impact**: KPIs and SDG alignment.
7. **Q&A**.
