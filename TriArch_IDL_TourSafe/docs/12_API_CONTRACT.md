# 12 — API Contract

> REST API contract for TourSafe backend and dashboard integration.

---

## 1. Base URLs

| Environment | URL |
|-------------|-----|
| Local | `http://localhost:8000` |
| Staging | `https://api-staging.toursafe.example` |
| Production | `https://api.toursafe.example` |

All endpoints are prefixed with `/api/v1` unless otherwise noted.

---

## 2. Authentication

Dashboard endpoints require JWT in header:
```
Authorization: Bearer <jwt>
```

Mobile WebSocket uses `traveler_id` in path and validates device signature on sensitive operations.

---

## 3. Health

### GET /health
**Response 200**
```json
{
  "status": "ok",
  "version": "0.1.0",
  "services": {
    "mongodb": "ok",
    "redis": "ok",
    "onnx": "ok"
  }
}
```

---

## 4. Travelers

### POST /travelers
Register a new traveler.

**Request**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "date_of_birth": "1990-01-01",
  "home_country": "India",
  "wallet_address": "0x...",
  "public_key_hash": "0x...",
  "did": "did:polygon:0x..."
}
```

**Response 201**
```json
{
  "id": "uuid",
  "did": "did:polygon:0x...",
  "created_at": "2026-08-11T12:00:00.000Z"
}
```

### GET /travelers/{id}
**Response 200**
```json
{
  "id": "uuid",
  "did": "did:polygon:0x...",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-9876543210",
  "home_country": "India",
  "created_at": "2026-08-11T12:00:00.000Z"
}
```

### PATCH /travelers/{id}
Update traveler profile (non-medical).

---

## 5. Trips

### POST /trips
**Request**
```json
{
  "traveler_id": "uuid",
  "name": "Kodaikanal Trek",
  "destination": "Kodaikanal, Tamil Nadu",
  "destination_geo": {"lat": 10.2381, "lng": 77.4892},
  "start_date": "2026-08-15T06:00:00.000Z",
  "end_date": "2026-08-18T18:00:00.000Z"
}
```

**Response 201**
```json
{
  "id": "uuid",
  "status": "ACTIVE",
  "created_at": "2026-08-11T12:00:00.000Z"
}
```

### GET /trips/{id}
Returns trip with latest GPS.

---

## 6. Geo-Fences

### GET /geo-fences
Query params: `jurisdiction`, `type`, `active`

**Response 200**
```json
{
  "fences": [
    {
      "id": "fence-001",
      "name": "Kolukkumalai Cliff Edge",
      "type": "HAZARD",
      "severity": "HIGH",
      "geometry": {...},
      "dwell_threshold_minutes": 10
    }
  ]
}
```

### POST /geo-fences
Admin only.

**Request**
```json
{
  "name": "...",
  "type": "HAZARD",
  "severity": "HIGH",
  "geometry": {...},
  "dwell_threshold_minutes": 10,
  "jurisdiction": "Tamil Nadu"
}
```

---

## 7. Incidents

### GET /incidents
Query params: `traveler_id`, `trip_id`, `status`, `type`, `from`, `to`, `limit`, `offset`

**Response 200**
```json
{
  "items": [...],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

### GET /incidents/{id}
**Response 200**
```json
{
  "incident_id": "uuid",
  "traveler_id": "uuid",
  "trip_id": "uuid",
  "type": "CRASH",
  "severity": "CRITICAL",
  "status": "CONFIRMED",
  "detected_at": "...",
  "confirmed_at": "...",
  "gps": {...},
  "reconstruction_error": 0.045,
  "threshold": 0.012
}
```

### POST /incidents/{id}/confirm
Dashboard operator confirms incident for full dispatch.

**Request**
```json
{"operator_id": "uuid", "notes": "..."}
```

**Response 200**
```json
{"status": "RESPONDING", "dispatched_at": "..."}
```

### POST /incidents/{id}/resolve
Mark incident resolved.

---

## 8. Offline Reconciliation

### POST /offline-reconcile
Accepts batched offline telemetry windows.

**Request**
```json
{
  "traveler_id": "uuid",
  "trip_id": "uuid",
  "windows": [
    {
      "window_index": 1,
      "timestamp": "2026-08-11T12:00:00.000Z",
      "gps": {"lat": 10.0, "lng": 78.0},
      "amag": [9.81, "...150"]
    }
  ]
}
```

**Response 200**
```json
{
  "accepted": 50,
  "rejected": 0,
  "anomalies_detected": 1
}
```

---

## 9. Emergency Resources

### GET /emergency-resources
Query params: `type`, `jurisdiction`, `lat`, `lng`, `radius_km`

**Response 200**
```json
{
  "resources": [
    {"id": "...", "type": "POLICE", "name": "...", "lat": 10.0, "lng": 78.0, "distance_km": 2.3}
  ]
}
```

---

## 10. Agencies

### POST /agencies/login
**Request**
```json
{"email": "...", "password": "..."}
```

**Response 200**
```json
{
  "access_token": "jwt",
  "agency": {"id": "...", "name": "...", "type": "..."}
}
```

---

## 11. Error Format

All errors follow:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "...",
    "details": {...}
  }
}
```

Common codes:
- `VALIDATION_ERROR` — 422
- `NOT_FOUND` — 404
- `UNAUTHORIZED` — 401
- `FORBIDDEN` — 403
- `INTERNAL_ERROR` — 500
