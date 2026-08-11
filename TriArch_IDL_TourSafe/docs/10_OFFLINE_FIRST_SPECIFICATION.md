# 10 — Offline-First Specification

> How TourSafe survives and recovers from zero-connectivity scenarios.

---

## 1. Principle

Travelers are most vulnerable where network coverage is weakest. TourSafe must continue capturing telemetry, detecting anomalies locally where possible, and synchronizing once connectivity returns.

---

## 2. Offline Scenarios

| Scenario | Behavior |
|----------|----------|
| Intermittent cellular | Queue windows, flush when stable. |
| Remote no-signal zone | Accumulate encrypted queue indefinitely (storage-limited). |
| Airplane mode | Queue all data; alert user that SOS requires network or manual action. |
| Backend unreachable | Retry with exponential backoff; preserve queue. |

---

## 3. Mobile Offline Buffer

### Storage
- SQLite table `telemetry_queue`.
- Encrypted with AES-256-CBC.

### Queue Entry Schema
```typescript
interface QueueEntry {
  id?: number;
  traveler_id: string;
  trip_id: string;
  payload_cipher: string; // base64
  iv: string;             // base64
  created_at: string;     // ISO8601
  status: 'PENDING' | 'IN_FLIGHT' | 'COMMITTED' | 'FAILED';
  retry_count: number;
}
```

### Encryption
```typescript
function encryptPayload(payload: object, key: Buffer, iv: Buffer): string {
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  const encrypted = Buffer.concat([
    cipher.update(JSON.stringify(payload), 'utf8'),
    cipher.final()
  ]);
  return encrypted.toString('base64');
}
```

### Key Derivation
- Master secret stored in SecureStore.
- Per-trip salt generated at trip start.
- Derived via PBKDF2 or HKDF.

---

## 4. Network Detection

### Ping Strategy
- Before each WebSocket send, attempt lightweight GET `/health`.
- Timeout: 3 seconds.
- If fail → queue payload.

### Connectivity Events
- Use NetInfo to listen for online/offline transitions.
- On online event → trigger immediate autocommit.

---

## 5. Autocommit Mechanism

### Schedule
- Every 30 seconds when app foreground/background active.
- Triggered immediately on connectivity restoration.

### Algorithm
```typescript
async function autocommit() {
  if (!(await isOnline())) return;
  const batch = await db.getPendingBatch(50);
  for (const row of batch) {
    await db.markInFlight(row.id);
    try {
      await ws.send(decrypt(row));
      await db.markCommitted(row.id);
    } catch (e) {
      await db.incrementRetry(row.id);
      if (row.retry_count >= MAX_RETRIES) {
        await db.markFailed(row.id);
      }
    }
  }
}
```

### Ordering
- Transmit oldest first to preserve timeline.
- Each row is acknowledged individually.

---

## 6. Offline Anomaly Detection (Stretch)

- Lightweight model inference on mobile is not required for MVP.
- If implemented in future, use TensorFlow Lite quantized model.
- For MVP, anomaly detection occurs server-side after flush.

### Immediate Safety
- Manual SOS still works if network available.
- If no network, SOS is queued and retried aggressively.
- Local geo-fence alerts work fully offline.

---

## 7. Storage Limits

- Max queue size: configurable (default 10,000 windows ≈ 7.5 MB).
- When limit reached, warn traveler and stop non-essential logging.
- On low storage, keep only last 24 hours.

---

## 8. Recovery Guarantees

| Metric | Target |
|--------|--------|
| Offline data recovery rate | > 99.9% |
| Max queued duration | Limited only by storage |
| Reconnection detection | < 30 s |
| Flush order | Chronological |

---

## 9. Testing

- Simulate network loss during trip.
- Verify queue growth.
- Restore network and verify flush.
- Verify server reconstructs timeline correctly.
- Verify anomaly detected from flushed data.
