# 14 — Security & Privacy

> Security model, privacy guarantees, and compliance posture for TourSafe.

---

## 1. Threat Model

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Traveler data breach | Critical | Encryption at rest and in transit; no plaintext medical data on servers |
| Identity spoofing | High | secp256k1 signatures; DID verification on-chain |
| Unauthorized vault decryption | Critical | Access grants gated by smart contract; time-limited; audit logged |
| Man-in-the-middle | High | TLS 1.3 everywhere; certificate pinning in mobile app |
| Replay of QR code | Medium | Timestamped signed tokens with 120-second expiry |
| Smart contract exploit | Critical | Audit; formal verification; bug bounty |
| Insider abuse | High | Smart contract enforces access rules; admin actions logged |
| Device theft | Medium | Secure enclave private key; biometrics optional |

---

## 2. Data Classification

| Data Class | Examples | Handling |
|------------|----------|----------|
| Highly Sensitive | Medical history, allergies, blood type, emergency contacts | Encrypted in IPFS vault; decrypted only during emergencies |
| Sensitive | GPS history, raw IMU | Encrypted offline buffer; purged 24h after trip |
| Moderate | DID, wallet address, public key | Public on blockchain |
| Internal | Incident logs, e-FIRs | Encrypted at rest; role-based access |
| Public | Geo-fence boundaries, resource locations | Open to authorized agencies |

---

## 3. Encryption Standards

### In Transit
- TLS 1.3 for all HTTP/WebSocket traffic.
- Certificate pinning in mobile app for production API.

### At Rest
- MongoDB: TLS + role-based access control; encrypted volumes.
- Redis: TLS + AUTH; no persistent sensitive data.
- SQLite: AES-256-CBC encrypted payloads.
- IPFS: Content encrypted; only CID is public.

### In Use
- Traveler private key: device secure enclave.
- Agency emergency key: encrypted secret manager (e.g., AWS Secrets Manager).

---

## 4. Identity & Access Management

### Travelers
- DID + keypair generated on device.
- No TourSafe server can decrypt medical vault without agency key + smart contract grant.

### Agencies
- JWT authentication for dashboard.
- Wallet address whitelisted in smart contract.
- Emergency key stored server-side but access logged on-chain.

### Administrators
- Multi-sig or hardware wallet for contract admin.
- Separate admin dashboard with MFA.

---

## 5. Privacy Architecture

### Zero-Knowledge Design
- Verifier can confirm DID is valid and emergency access is active without seeing underlying data.
- QR signature proves possession of private key without revealing it.

### Ephemeral Data
- Raw telemetry purged 24 hours after trip end.
- Only anonymized aggregates retained for heatmaps.

### On-Chain Audit
- Every `grantEmergencyAccess` and `revokeEmergencyAccess` recorded immutably.
- Traveler can review access history.

---

## 6. Compliance

| Regulation | Requirement | TourSafe Approach |
|------------|-------------|-------------------|
| GDPR | Data minimization, right to erasure | Purge telemetry; delete vault CID mapping on request |
| PDPA (India) | Consent, data localization | Consent at onboarding; region-matched cloud regions |
| HIPAA-like | Medical data protection | Encryption, access logs, minimum necessary disclosure |
| CCPA | Disclosure, deletion | Provide data export; honor deletion requests |

---

## 7. Incident Response

1. Detect anomaly or breach via monitoring/audit.
2. Revoke compromised agency keys.
3. Rotate encryption keys if needed.
4. Notify affected travelers per jurisdiction law.
5. Document post-incident report.

---

## 8. Security Checklist

- [ ] TLS 1.3 on all services.
- [ ] Secrets managed via environment variables / secret manager.
- [ ] Smart contract audited before mainnet.
- [ ] Dependency scanning in CI.
- [ ] Rate limiting on APIs.
- [ ] Input validation via Pydantic.
- [ ] SQL injection prevention via parameterized queries.
- [ ] XSS/CSRF protection in dashboard.
- [ ] Biometric lock option in mobile app.
