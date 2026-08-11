# 05 — Backend Specification

> Specification for the FastAPI real-time backend, Redis cache, MongoDB persistence, and dashboard-facing services.

---

## 1. Overview

The backend ingests high-frequency telemetry from mobile clients, evaluates it through ML inference, maintains live state, emits incidents to authorities, and archives everything for analytics and compliance.

### Primary Responsibilities
1. Persistent WebSocket telemetry ingestion.
2. Real-time GPS caching in Redis.
3. ML anomaly inference via ONNX Runtime.
4. Incident detection, confirmation, and emission.
5. REST API for dashboard queries.
6. Offline-queue reconciliation.
7. Triggering e-FIR generation.

---

## 2. Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + lifespan
│   ├── config.py            # Pydantic settings
│   ├── dependencies.py      # shared deps (db, redis)
│   ├── routers/
│   │   ├── telemetry.py     # WebSocket handler
│   │   ├── travelers.py     # CRUD
│   │   ├── incidents.py     # incident queries
│   │   ├── geo_fences.py    # geo-fence CRUD
│   │   └── health.py        # health checks
│   ├── services/
│   │   ├── inference.py     # ONNX worker pool
│   │   ├── anomaly.py       # confirmation logic
│   │   ├── dispatcher.py    # event emission
│   │   ├── geo_service.py   # server-side geo-fence checks
│   │   └── efir_trigger.py  # call e-FIR microservice
│   ├── models/
│   │   ├── telemetry.py     # Pydantic telemetry models
│   │   ├── traveler.py
│   │   └── incident.py
│   └── core/
│       ├── db.py            # MongoDB connection
│       └── cache.py         # Redis connection
├── models/
│   └── lstm_autoencoder.onnx
├── tests/
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

---

## 3. FastAPI Application

### Lifespan
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    load_onnx_model()
    yield
    await close_db()
    await close_redis()
```

### Middleware
- CORS for dashboard origin.
- Request ID logging.
- Exception handler returning structured errors.

---

## 4. WebSocket Telemetry Handler

### Endpoint
```
WS /ws/telemetry/{traveler_id}
```

### Connection Lifecycle
1. Validate `traveler_id` exists.
2. Accept connection.
3. Register connection in connection manager.
4. Start heartbeat task (ping every 30 s).
5. Process incoming messages until disconnect.

### Incoming Messages
```json
{
  "type": "telemetry_window",
  "trip_id": "uuid",
  "window_index": 42,
  "timestamp": "2026-08-11T12:34:56.789Z",
  "gps": {"lat": 12.3456, "lng": 78.9012, "accuracy": 4.5},
  "amag": [9.81, 9.82, "..."]
}
```

### Processing Pipeline
```
Receive window
   ↓
Validate Pydantic model
   ↓
Update Redis GPS (TTL 300 s)
   ↓
Archive window to MongoDB telemetry_archive
   ↓
Submit to ONNX inference worker
   ↓
Receive reconstruction error
   ↓
Evaluate anomaly confirmation
   ↓
If confirmed → emit incident
```

### Outgoing Messages
- `config_update` — threshold, geo-fence refresh.
- `alert` — anomaly warning or confirmation.
- `pong` — heartbeat response.

---

## 5. ML Inference Service

### Worker Pool
- Use `asyncio` + `ThreadPoolExecutor` or ONNX `InferenceSession` in each worker.
- Default 4 workers; configurable via `INFERENCE_WORKERS`.
- Preload model once; sessions may be per-worker for thread safety.

### Input Normalization
- Ensure window length = 150.
- Reshape to `(1, 150, 1)` float32.
- Optional: z-score normalize using training mean/std.

### Output
- `reconstruction_error: float` — MSE between input and reconstruction.
- Latency target: < 100 ms.

---

## 6. Anomaly Confirmation Logic

### Per-Traveler State
- Maintain latest reconstruction error and previous window error in Redis or in-memory.
- Reset if gap > 10 seconds between windows.

### Confirmation Rules
```python
if current_error > threshold and previous_error > threshold:
    confirm_anomaly(traveler_id, current_error, window)
elif current_error > threshold:
    flag_first_stage(traveler_id)
```

### Event Types
- `CRASH` — high G-force spike + chaotic/immobile aftermath.
- `IMMOBILITY` — A_mag flatline at ~9.81 m/s² + static remote GPS.
- `GEOFENCE_BREACH` — server-side confirmation of client geo-fence event.
- `MANUAL_SOS` — immediate, no confirmation needed.

---

## 7. Incident Emission

### Incident Packet Structure
See `03_TECHNICAL_SPECIFICATION.md` Section 7.

### Emitters
1. **Socket.io Relay** — push to MERN dashboard subscribers for the zone.
2. **e-FIR Trigger** — HTTP call to Node.js e-FIR microservice.
3. **Blockchain Access Grant** — call `grantEmergencyAccess` on smart contract.

### Ordering
- Emit dashboard alert immediately.
- Grant blockchain access in background.
- Trigger e-FIR after access grant transaction is mined or after timeout fallback.

---

## 8. Redis Cache

### Keys
| Key Pattern | Value | TTL |
|-------------|-------|-----|
| `gps:{traveler_id}` | JSON `{lat, lng, timestamp}` | 300 s |
| `conn:{traveler_id}` | WebSocket connection metadata | connection lifetime |
| `anomaly:first_stage:{traveler_id}` | JSON `{error, timestamp}` | 60 s |

### Eviction
- Use Redis `EX` or `PX` for TTL.
- On traveler logout/trip end, manually delete keys.

---

## 9. MongoDB Collections

### travelers
```json
{
  "_id": "uuid",
  "did": "did:polygon:...",
  "name": "...",
  "email": "...",
  "phone": "...",
  "home_country": "...",
  "emergency_contacts": [...],
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### trips
```json
{
  "_id": "uuid",
  "traveler_id": "uuid",
  "destination": "...",
  "start_date": "ISODate",
  "end_date": "ISODate",
  "status": "ACTIVE | COMPLETED | CANCELLED",
  "created_at": "ISODate"
}
```

### telemetry_archive
```json
{
  "traveler_id": "uuid",
  "trip_id": "uuid",
  "window_index": 42,
  "timestamp": "ISODate",
  "gps": {...},
  "amag": [...],
  "reconstruction_error": 0.002
}
```

### incidents
```json
{
  "_id": "uuid",
  "traveler_id": "uuid",
  "trip_id": "uuid",
  "type": "CRASH | IMMOBILITY | GEOFENCE_BREACH | MANUAL_SOS",
  "severity": "CRITICAL | HIGH | MEDIUM",
  "status": "DETECTED | CONFIRMED | RESPONDING | RESOLVED",
  "gps": {...},
  "reconstruction_error": 0.045,
  "threshold": 0.012,
  "created_at": "ISODate",
  "resolved_at": "ISODate | null"
}
```

### efir_archive
```json
{
  "incident_id": "uuid",
  "payload_json": {...},
  "pdf_url": "...",
  "dispatch_status": {...},
  "created_at": "ISODate"
}
```

### geo_fences
```json
{
  "_id": "uuid",
  "name": "...",
  "type": "HAZARD | SAFE_ZONE",
  "geometry": {"type": "Polygon", "coordinates": [...]},
  "metadata": {...},
  "active": true
}
```

---

## 10. REST API Contract Summary

Full details in `12_API_CONTRACT.md`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service health |
| POST | `/api/v1/travelers` | Register traveler |
| GET | `/api/v1/travelers/{id}` | Get profile |
| PATCH | `/api/v1/travelers/{id}` | Update profile |
| GET | `/api/v1/geo-fences` | List active fences |
| POST | `/api/v1/geo-fences` | Create fence (admin) |
| GET | `/api/v1/incidents` | List incidents |
| GET | `/api/v1/incidents/{id}` | Get incident |
| POST | `/api/v1/incidents/{id}/confirm` | Confirm dispatch |
| POST | `/api/v1/offline-reconcile` | Accept batched offline windows |

---

## 11. Dashboard Integration

### Socket.io Events (FastAPI → Dashboard)
- `incident:new` — new confirmed incident.
- `incident:update` — status change.
- `traveler:status` — safety status change (green/amber/red).

### Dashboard REST Consumers
- Dashboard queries `/api/v1/incidents`, `/api/v1/travelers`, `/api/v1/geo-fences`.

---

## 12. Offline Reconciliation

### Endpoint
```
POST /api/v1/offline-reconcile
```

### Body
```json
{
  "traveler_id": "uuid",
  "trip_id": "uuid",
  "windows": [
    {"timestamp": "...", "gps": {...}, "amag": [...]}
  ]
}
```

### Behavior
- Validate traveler/trip.
- Insert windows into `telemetry_archive`.
- Run inference on each window.
- If anomaly found, emit incident retroactively.
- Return summary: accepted count, anomalies detected.

---

## 13. Error Handling

- Pydantic `ValidationError` → 422 with field details.
- WebSocket invalid message → log + close code 1003.
- ONNX inference failure → return fallback error + alert ops.
- Redis/MongoDB unreachable → fail health check; queue in memory briefly.

---

## 14. Observability

- Structured JSON logging via `structlog` or standard `logging`.
- Metrics: telemetry ingress rate, inference latency, anomaly count, incident latency.
- Optional: Prometheus `/metrics` endpoint.
