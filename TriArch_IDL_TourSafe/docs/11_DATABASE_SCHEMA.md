# 11 — Database Schema

> MongoDB, Redis, and SQLite schemas for TourSafe.

---

## 1. MongoDB

Database name: `toursafe`

### 1.1 travelers
```json
{
  "_id": "ObjectId",
  "did": "did:polygon:0x...",
  "wallet_address": "0x...",
  "public_key_hash": "0x...",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-...",
  "date_of_birth": "1990-01-01",
  "home_country": "India",
  "nationality": "Indian",
  "created_at": "ISODate",
  "updated_at": "ISODate",
  "is_active": true
}
```
Indexes: `did` (unique), `wallet_address` (unique), `phone`

### 1.2 trips
```json
{
  "_id": "ObjectId",
  "traveler_id": "ObjectId",
  "name": "Kodaikanal Trek",
  "destination": "Kodaikanal, Tamil Nadu",
  "destination_geo": {"lat": 10.2381, "lng": 77.4892},
  "start_date": "ISODate",
  "end_date": "ISODate",
  "status": "SCHEDULED | ACTIVE | COMPLETED | CANCELLED",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```
Indexes: `traveler_id`, `status`, `start_date`

### 1.3 telemetry_archive
```json
{
  "_id": "ObjectId",
  "traveler_id": "ObjectId",
  "trip_id": "ObjectId",
  "window_index": 42,
  "timestamp": "ISODate",
  "gps": {
    "lat": 10.1234,
    "lng": 78.1234,
    "accuracy": 4.5
  },
  "amag": [9.81, 9.82, "...150 floats"],
  "reconstruction_error": 0.002,
  "received_at": "ISODate",
  "offline_data": false
}
```
Indexes: `traveler_id + trip_id + timestamp` (compound), `trip_id`
TTL: 30 days after `end_date` (via nightly job)

### 1.4 incidents
```json
{
  "_id": "ObjectId",
  "incident_id": "uuid",
  "traveler_id": "ObjectId",
  "trip_id": "ObjectId",
  "type": "CRASH | IMMOBILITY | GEOFENCE_BREACH | MANUAL_SOS",
  "severity": "CRITICAL | HIGH | MEDIUM",
  "status": "DETECTED | CONFIRMED | RESPONDING | RESOLVED",
  "detected_at": "ISODate",
  "confirmed_at": "ISODate",
  "resolved_at": "ISODate | null",
  "gps": {"lat": 10.1234, "lng": 78.1234, "accuracy": 4.5},
  "reconstruction_error": 0.045,
  "threshold": 0.012,
  "lstm_window": ["...150 floats"],
  "geo_fence_violations": ["fence-001"],
  "offline_data_flag": false,
  "created_at": "ISODate"
}
```
Indexes: `traveler_id`, `trip_id`, `status`, `type`, `created_at`

### 1.5 efir_archive
```json
{
  "_id": "ObjectId",
  "incident_id": "uuid",
  "traveler_id": "ObjectId",
  "trip_id": "ObjectId",
  "payload_json": { "..." },
  "pdf_url": "https://...",
  "dispatch_targets": {
    "police": {"id": "...", "name": "...", "distance_km": 2.3, "endpoint": "...", "dispatched_at": "ISODate"},
    "hospital": {"id": "...", "name": "...", "distance_km": 4.1, "endpoint": "...", "dispatched_at": "ISODate"}
  },
  "dispatch_status": "PENDING | SENT | FAILED | ACKNOWLEDGED",
  "created_at": "ISODate"
}
```
Indexes: `incident_id` (unique), `traveler_id`, `dispatch_status`

### 1.6 geo_fences
```json
{
  "_id": "ObjectId",
  "fence_id": "uuid",
  "name": "Kolukkumalai Cliff Edge",
  "type": "HAZARD | SAFE_ZONE | ROUTE_CORRIDOR | NO_GO",
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[["..."]]]
  },
  "dwell_threshold_minutes": 10,
  "jurisdiction": "Tamil Nadu",
  "active": true,
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```
Indexes: `type`, `active`, `jurisdiction`

### 1.7 emergency_resources
```json
{
  "_id": "ObjectId",
  "resource_id": "uuid",
  "type": "POLICE | HOSPITAL | EMS | FIRE",
  "name": "Kodaikanal Government Hospital",
  "lat": 10.2345,
  "lng": 78.3456,
  "address": "...",
  "phone": "...",
  "api_endpoint": "https://...",
  "jurisdiction": "Tamil Nadu",
  "active": true
}
```
Indexes: `type + jurisdiction + active` (compound), `lat/lng` (2dsphere)

### 1.8 agencies
```json
{
  "_id": "ObjectId",
  "agency_id": "uuid",
  "name": "Tamil Nadu Police",
  "type": "POLICE | HOSPITAL | TOURISM",
  "wallet_address": "0x...",
  "emergency_access_key": "<encrypted>",
  "jurisdiction": "Tamil Nadu",
  "active": true,
  "created_at": "ISODate"
}
```

### 1.9 audit_logs
```json
{
  "_id": "ObjectId",
  "event_type": "DID_ACCESS | EMISSION | DISPATCH | LOGIN | LOGOUT",
  "actor": "agency-id or system",
  "target_traveler_id": "ObjectId",
  "metadata": {},
  "tx_hash": "0x...",
  "created_at": "ISODate"
}
```
Indexes: `event_type`, `target_traveler_id`, `created_at`

---

## 2. Redis

### Key Patterns
| Pattern | Type | Value | TTL |
|---------|------|-------|-----|
| `gps:{traveler_id}` | String | JSON `{lat,lng,timestamp,speed}` | 300 s |
| `conn:{traveler_id}` | String | JSON `{connected_at, socket_id}` | connection lifetime |
| `anomaly:first_stage:{traveler_id}` | String | JSON `{error, window_index, timestamp}` | 60 s |
| `geo_fence:entry:{traveler_id}:{fence_id}` | String | ISO8601 entry timestamp | 3600 s |
| `rate_limit:ws:{traveler_id}` | String | count | 60 s |

---

## 3. SQLite (Mobile Offline Queue)

```sql
CREATE TABLE telemetry_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    traveler_id TEXT NOT NULL,
    trip_id TEXT NOT NULL,
    payload_cipher TEXT NOT NULL,
    iv TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT CHECK(status IN ('PENDING','IN_FLIGHT','COMMITTED','FAILED')) DEFAULT 'PENDING',
    retry_count INTEGER DEFAULT 0
);

CREATE INDEX idx_status_created ON telemetry_queue(status, created_at);
CREATE INDEX idx_trip ON telemetry_queue(trip_id);
```

---

## 4. Data Retention

| Data | Retention |
|------|-----------|
| Raw telemetry_archive | Until 24 h after trip end |
| incidents | Permanent |
| efir_archive | Permanent |
| Redis GPS | 5 minutes |
| audit_logs | Permanent |
| Anonymized heatmap aggregates | Permanent |
