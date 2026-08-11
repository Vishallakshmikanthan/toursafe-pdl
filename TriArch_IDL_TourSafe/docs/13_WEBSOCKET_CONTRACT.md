# 13 — WebSocket Contract

> Message formats and event semantics for TourSafe real-time channels.

---

## 1. Channels

### 1.1 Mobile ↔ FastAPI
- URL: `wss://api.toursafe.example/ws/telemetry/{traveler_id}`
- Protocol: native WebSocket (JSON messages)
- Heartbeat: ping/pong every 30 seconds

### 1.2 FastAPI ↔ Dashboard (via Node relay)
- Library: Socket.io
- URL: `https://api.toursafe.example/socket.io`
- Rooms: `zone:{jurisdiction}`, `incident:{incident_id}`

---

## 2. Mobile → Backend Messages

### 2.1 telemetry_window
```json
{
  "type": "telemetry_window",
  "trip_id": "uuid",
  "window_index": 42,
  "timestamp": "2026-08-11T12:34:56.789Z",
  "gps": {
    "lat": 12.3456,
    "lng": 78.9012,
    "accuracy": 4.5
  },
  "amag": [9.81, 9.82, "...150 floats"]
}
```

### 2.2 geo_fence_breach
```json
{
  "type": "geo_fence_breach",
  "trip_id": "uuid",
  "fence_id": "fence-001",
  "event": "ENTERED | EXITED",
  "timestamp": "2026-08-11T12:34:56.789Z",
  "gps": {"lat": 12.3456, "lng": 78.9012}
}
```

### 2.3 sos_manual
```json
{
  "type": "sos_manual",
  "trip_id": "uuid",
  "timestamp": "2026-08-11T12:34:56.789Z",
  "gps": {"lat": 12.3456, "lng": 78.9012},
  "message": "optional message"
}
```

### 2.4 ping
```json
{"type": "ping", "timestamp": "..."}
```

---

## 3. Backend → Mobile Messages

### 3.1 pong
```json
{"type": "pong", "timestamp": "..."}
```

### 3.2 config_update
```json
{
  "type": "config_update",
  "anomaly_threshold": 0.012,
  "geo_fences_version": "2026-08-11T00:00:00Z",
  "sensor_polling_hz": 50
}
```

### 3.3 alert
```json
{
  "type": "alert",
  "level": "WARNING | CRITICAL",
  "title": "Anomaly Detected",
  "message": "Emergency services have been notified.",
  "incident_id": "uuid",
  "timestamp": "..."
}
```

---

## 4. Backend → Dashboard Socket.io Events

### 4.1 incident:new
```json
{
  "incident_id": "uuid",
  "traveler_id": "uuid",
  "trip_id": "uuid",
  "type": "CRASH",
  "severity": "CRITICAL",
  "status": "CONFIRMED",
  "timestamp": "2026-08-11T12:34:56.789Z",
  "gps": {"lat": 12.3456, "lng": 78.9012},
  "reconstruction_error": 0.045
}
```

### 4.2 incident:update
```json
{
  "incident_id": "uuid",
  "status": "RESPONDING",
  "updated_at": "...",
  "operator_id": "uuid"
}
```

### 4.3 traveler:status
```json
{
  "traveler_id": "uuid",
  "status": "GREEN | AMBER | RED",
  "last_gps": {"lat": 12.3456, "lng": 78.9012, "timestamp": "..."},
  "geo_fence_alerts": ["fence-001"]
}
```

### 4.4 efir:dispatched
```json
{
  "incident_id": "uuid",
  "police_status": "SENT | ACKNOWLEDGED | FAILED",
  "hospital_status": "SENT | ACKNOWLEDGED | FAILED",
  "dispatched_at": "..."
}
```

---

## 5. Dashboard → Backend Events

### 5.1 subscribe:zone
```json
{"event": "subscribe:zone", "jurisdiction": "Tamil Nadu"}
```

### 5.2 confirm:incident
```json
{"event": "confirm:incident", "incident_id": "uuid", "operator_id": "uuid"}
```

### 5.3 resolve:incident
```json
{"event": "resolve:incident", "incident_id": "uuid", "operator_id": "uuid"}
```

---

## 6. Reconnection Semantics

- Mobile: exponential backoff starting at 1 s, max 30 s.
- Dashboard Socket.io: automatic reconnect with `reconnectionAttempts: 10`.
- On reconnect, mobile resubmits `trip_id` and pending queue.

---

## 7. Error Codes

| Code | Meaning |
|------|---------|
| 1000 | Normal closure |
| 1003 | Invalid message type |
| 1006 | Abnormal disconnect |
| 1008 | Policy violation (invalid traveler_id) |
| 1011 | Server error |
