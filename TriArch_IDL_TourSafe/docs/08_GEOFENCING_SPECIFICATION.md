# 08 — Geo-Fencing Specification

> Specification for virtual hazard perimeters, safe zones, and boundary detection.

---

## 1. Overview

Geo-fences are virtual geographic boundaries that define hazardous zones and certified safe zones. TourSafe evaluates traveler position against these boundaries to generate alerts and inform response prioritization.

---

## 2. Types of Geo-Fences

| Type | Purpose | Alert Level |
|------|---------|-------------|
| **Hazard Zone** | Avalanche areas, cliffs, flood zones, restricted wildlife areas | Amber → Red if prolonged |
| **Safe Zone** | Certified tourism corridors with active monitoring | Green baseline |
| **Route Corridor** | Expected path between points | Deviations flagged |
| **No-Go Zone** | Legally restricted areas | Red immediate |

---

## 3. Data Format

Geo-fences are stored as GeoJSON `FeatureCollection` objects.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": "fence-001",
        "name": "Kolukkumalai Cliff Edge",
        "type": "HAZARD",
        "severity": "HIGH",
        "dwell_threshold_minutes": 10,
        "active": true
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [78.1234, 10.1234],
            [78.1240, 10.1234],
            [78.1240, 10.1240],
            [78.1234, 10.1240],
            [78.1234, 10.1234]
          ]
        ]
      }
    }
  ]
}
```

---

## 4. Client-Side Evaluation

### Library
- `@turf/turf` React Native compatible build.
- Specifically `turf.booleanPointInPolygon(point, polygon)`.

### Flow
1. At trip start, fetch active geo-fences from backend.
2. Cache in SQLite + Redux store.
3. On each GPS update:
   - Build Turf `point([lng, lat])`.
   - Evaluate against each cached polygon.
   - Detect state transitions: `OUTSIDE → INSIDE`, `INSIDE → OUTSIDE`.

### Alerts
- Enter hazard zone → local notification + transmit breach event.
- Remain inside hazard zone > dwell threshold → escalate to HIGH.
- Exit hazard zone → clear alert.

---

## 5. Server-Side Evaluation

### Purpose
- Confirm client-reported breaches.
- Detect breaches from hardware prototype or manual entries.
- Provide authoritative record for incident timeline.

### Library
- Python `shapely` or `geojson` + custom point-in-polygon.

### Endpoint
```
POST /api/v1/geo-fences/check
```
Body:
```json
{"lat": 10.1234, "lng": 78.1234}
```

Response:
```json
{"inside": ["fence-001"], "outside": ["..."]}
```

---

## 6. Dashboard Visualization

- Render GeoJSON polygons on Mapbox GL JS map.
- Hazard zones: red/orange translucent fill.
- Safe zones: green translucent fill.
- Breached fences: pulsing border.

---

## 7. Dwell Time Escalation

- Track entry timestamp per traveler per fence in Redis.
- If `(now - entry_time) > dwell_threshold`:
  - Escalate status to HIGH.
  - Notify dashboard duty officer.
  - Push notification to traveler if still online.

---

## 8. Performance Considerations

- Cache fences locally on device to avoid repeated network calls.
- Limit number of active fences per trip to < 100 for client performance.
- Simplify complex polygons if needed (Douglas-Peucker).

---

## 9. Privacy

- Geo-fence evaluation happens on device where possible.
- Server-side checks log only breach events, not continuous position.
- Aggregated heatmaps use anonymized data only.
