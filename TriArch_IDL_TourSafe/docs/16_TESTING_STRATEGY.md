# 16 — Testing Strategy

> Comprehensive testing plan for TourSafe modules and end-to-end flows.

---

## 1. Testing Levels

| Level | Focus | Owner |
|-------|-------|-------|
| Unit | Individual functions and classes | Member 1, Member 2 |
| Integration | Module interactions | Member 1, Member 2 |
| System | End-to-end flows | Member 3 + team |
| Load | Concurrency and throughput | Member 1 |
| Security | Vulnerability scans, access control | Member 1 |
| Hardware | Physical prototype validation | Member 3 |

---

## 2. Unit Tests

### Python (backend)
- A_mag calculation.
- Sliding window segmentation.
- Haversine distance.
- AES encryption/decryption round-trip.
- Pydantic model validation.
- Redis cache operations.

### TypeScript (mobile)
- Window processor.
- Geo-fence point-in-polygon.
- QR payload generation and verification.
- Redux reducers.

### Solidity (blockchain)
- registerDID, resolveDID.
- grant/revoke emergency access.
- Access control (onlyAdmin).
- Event emissions.

---

## 3. Integration Tests

### Telemetry Pipeline
1. Simulate 50Hz sensor stream from test client.
2. Verify FastAPI receives windows.
3. Verify Redis GPS update.
4. Verify MongoDB archive insertion.
5. Verify ONNX inference output.
6. Inject anomalous window; verify incident emission.

### Offline Buffer
1. Disconnect test client network.
2. Send telemetry; verify SQLite queue growth.
3. Reconnect; verify autocommit flush.
4. Verify server-side reconstruction and anomaly detection.

### DID Emergency Flow
1. Register DID on Hardhat/Amoy.
2. Upload encrypted vault to IPFS.
3. Trigger anomaly.
4. Grant emergency access.
5. Decrypt vault and verify content.

### e-FIR Dispatch
1. Confirm incident.
2. Verify e-FIR JSON and PDF generation.
3. Mock police/hospital API endpoints.
4. Verify dispatch requests and status logging.

---

## 4. Load Tests

### Tool
- Locust for FastAPI HTTP/WebSocket.
- Custom Node scripts for Socket.io.

### Scenarios
| Scenario | Load | Acceptance |
|----------|------|------------|
| Concurrent telemetry streams | 1,000 WebSockets, 50 Hz each | 99th percentile inference latency < 500 ms |
| Simultaneous anomalies | 10% of streams trigger anomalies | e-FIR generation succeeds for > 99% |
| Dashboard subscribers | 50 concurrent operators | Incident push latency < 1 s |
| Offline reconciliation | 10,000 windows per batch | Batch processed in < 60 s |

---

## 5. Security Tests

- Static analysis with `slither` on Solidity.
- Dependency audit with `npm audit`, `safety` (Python).
- JWT token tampering attempts.
- QR replay attacks (old timestamp).
- Unauthorized DID vault decryption attempts.

---

## 6. Hardware Tests

| Test | Method | Expected Result |
|------|--------|-----------------|
| Crash detection | High-G impulse | Dashboard CRITICAL alert |
| Immobility | Stationary device in remote zone | Dashboard alert after threshold |
| Offline recovery | Disable/enable Wi-Fi | Complete telemetry flush |
| Geo-fence | Spoof GPS across fence | Amber alert + local feedback |
| Manual SOS | Press button | Immediate CRITICAL alert |

---

## 7. Test Environments

| Environment | Components |
|-------------|------------|
| Local | Docker Compose, Hardhat local node, mock IPFS |
| Staging | K8s, Polygon Amoy, Pinata IPFS |
| Production | K8s, Polygon mainnet, managed IPFS |

---

## 8. CI/CD Testing

- Every PR triggers:
  - Python unit tests.
  - TypeScript unit tests.
  - Hardhat tests.
  - Linting.
  - Integration test subset.
- Nightly load tests on staging.

---

## 9. Test Data

- `tests/data/normal_activity.csv` — labeled normal sessions.
- `tests/data/crash_simulations.csv` — high-G events.
- `tests/data/mock_geo_fences.json` — test polygons.
- `tests/data/mock_agencies.json` — test agency accounts.

---

## 10. Exit Criteria

- > 80% unit test coverage.
- All integration tests passing.
- Load test acceptance criteria met.
- No critical/high security findings.
- Hardware validation log signed off by Member 3.
