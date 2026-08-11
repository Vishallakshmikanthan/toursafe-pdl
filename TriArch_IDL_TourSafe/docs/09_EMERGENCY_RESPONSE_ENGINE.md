# 09 — Emergency Response Engine

> Specification for incident detection, confirmation, e-FIR generation, dispatch, and responder workflow.

---

## 1. Overview

The Emergency Response Engine translates AI anomaly signals into structured, actionable incident reports dispatched to the nearest responders. It minimizes human administrative delay and preserves the Golden Hour.

---

## 2. Incident Triggers

| Source | Trigger Condition | Severity |
|--------|-------------------|----------|
| LSTM Autoencoder | Two consecutive windows above threshold | CRITICAL |
| Geo-fence dwell | Inside hazard zone > threshold | HIGH |
| Manual SOS | User presses override | CRITICAL |
| SNN-CAD | Trajectory deviation (stretch) | MEDIUM |

---

## 3. Incident State Machine

```
DETECTED → CONFIRMED → RESPONDING → RESOLVED
              ↑
        operator confirmation or auto-confirm
```

### States
- **DETECTED**: Anomaly signal received, awaiting confirmation.
- **CONFIRMED**: Two-stage threshold crossed or operator confirmed.
- **RESPONDING**: e-FIR dispatched, agency notified.
- **RESOLVED**: Emergency closed by operator.

---

## 4. Confirmation Logic

### Auto-Confirmation
- LSTM two-stage confirmation → auto-confirmed CRITICAL.
- Manual SOS → auto-confirmed CRITICAL.

### Operator Confirmation
- Dashboard shows amber alert for first-stage flags.
- Operator can confirm or dismiss within 60 seconds.
- If no operator action, auto-escalate after timeout.

---

## 5. e-FIR Generation

### Timing
- Generate immediately upon confirmed incident.

### Inputs
- Anomaly log (timestamp, GPS, LSTM error trace, window)
- Decrypted DID vault (medical data, contacts)
- Geo-fence status
- Offline data flag

### Outputs
1. **JSON payload** — machine-readable for police/hospital APIs.
2. **PDF report** — human-readable for jurisdictions requiring paper records.

### e-FIR JSON Schema
```json
{
  "incident_id": "uuid",
  "generated_at": "ISO8601",
  "source_system": "TourSafe",
  "traveler": {
    "did": "did:polygon:...",
    "name": "...",
    "date_of_birth": "...",
    "blood_type": "...",
    "allergies": [...],
    "conditions": [...],
    "medications": [...],
    "emergency_contacts": [...],
    "insurance": "..."
  },
  "incident": {
    "type": "CRASH | IMMOBILITY | GEOFENCE_BREACH | MANUAL_SOS",
    "detected_at": "ISO8601",
    "confirmed_at": "ISO8601",
    "gps": {"lat": ..., "lng": ..., "accuracy": ...},
    "location_description": "...",
    "reconstruction_error": 0.045,
    "threshold": 0.012,
    "geo_fence_violations": ["fence-001"],
    "offline_data_flag": false
  },
  "dispatch_targets": {
    "police": {"id": "...", "name": "...", "distance_km": 2.3, "endpoint": "..."},
    "hospital": {"id": "...", "name": "...", "distance_km": 4.1, "endpoint": "..."}
  }
}
```

---

## 6. Dispatch Routing

### Haversine Distance
```python
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
```

### Resource Database
- MongoDB collection `emergency_resources`.
- Fields: `type`, `name`, `lat`, `lng`, `jurisdiction`, `api_endpoint`, `active`.

### Selection
- Filter resources within jurisdiction.
- Rank by Haversine distance.
- Select nearest police and nearest hospital.

---

## 7. Dispatch Flow

```
Confirmed Incident
   ↓
Grant emergency blockchain access
   ↓
Decrypt DID vault
   ↓
Query emergency resources
   ↓
Rank by Haversine distance
   ↓
Generate JSON + PDF e-FIR
   ↓
POST JSON to police API
   ↓
POST JSON/PDF to hospital API
   ↓
Log dispatch status to MongoDB
   ↓
Emit dashboard update
```

---

## 8. Responder Workflow

### Dashboard Alert
- Real-time incident card appears.
- Map zooms to incident GPS.
- Operator reviews traveler profile and anomaly trace.

### QR Scan Decryption
- Responder opens `/qr-scan` on authorized device.
- Scans traveler QR code.
- Dashboard verifies signature and resolves DID.
- If emergency access active, decrypts vault from IPFS.
- Displays medical profile within 15 seconds.

### Manual Fallback
- If QR unreadable, responder can enter DID manually.
- Requires operator approval and logs extra audit event.

---

## 9. Resolution

- Operator marks incident RESOLVED in dashboard.
- Blockchain emergency access is revoked.
- Final incident record archived.
- Traveler notified if online.

---

## 10. Latency Targets

| Step | Target |
|------|--------|
| AI confirm → dashboard alert | < 1 s |
| Confirm → e-FIR generated | < 10 s |
| e-FIR → police/hospital receipt | < 60 s |
| QR scan → medical data display | < 15 s |
