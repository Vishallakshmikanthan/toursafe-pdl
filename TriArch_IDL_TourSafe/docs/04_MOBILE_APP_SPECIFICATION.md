# 04 — Mobile App Specification

> Detailed specification for the TourSafe React Native mobile application.

---

## 1. Overview

The mobile app is the primary sensor platform and traveler-facing interface. It must operate silently, preserve battery, function offline, and protect the traveler's identity data.

### Platform Targets
- Android 10+ (API 29+)
- iOS 14+

### Build Workflow
- React Native CLI bare workflow
- Hermes enabled
- TypeScript strict mode

---

## 2. App Modules

```
mobile/src/
├── api/                 # Backend and blockchain clients
├── components/          # Reusable UI components
├── screens/             # Top-level screens
├── navigation/          # React Navigation setup
├── store/               # Redux Toolkit slices
├── services/
│   ├── SensorService.ts
│   ├── WindowProcessor.ts
│   ├── NetworkInterceptor.ts
│   ├── OfflineQueue.ts
│   ├── GeoFenceEngine.ts
│   ├── DIDWallet.ts
│   └── NotificationService.ts
├── hooks/               # Custom React hooks
├── utils/               # Math, crypto, formatting helpers
├── constants/           # Config and constants
└── types/               # Shared TypeScript types
```

---

## 3. Screens

### 3.1 Onboarding Flow
| Screen | Purpose |
|--------|---------|
| Welcome | Intro + permissions rationale |
| Permissions | Location + motion + notification |
| DID Create | Generate secp256k1 keypair, store in SecureStore |
| Medical Profile | Blood type, allergies, conditions, medications |
| Emergency Contacts | Name, phone, relation |
| Trip Setup | Trip name, start/end dates, destination |
| QR Preview | Show generated DID QR code |

### 3.2 Main Screens
| Screen | Purpose |
|--------|---------|
| Home | Safety status, active alerts, connection, queue length |
| Live Map | Self-location, nearby safe zones, hazard polygons |
| Emergency Override | Manual SOS with countdown + cancel |
| Profile | View/edit medical data, regenerate QR |
| Settings | Permissions, sensor tuning, logout |

---

## 4. Sensor Service

### 4.1 Accelerometer
- Polling target: 50 Hz
- Raw data: `{x, y, z, timestamp}` in m/s²
- Listener started on trip activation
- Listener paused/stopped based on app lifecycle and adaptive polling

### 4.2 GPS Location
- Polling target: 1 Hz
- Configuration:
  - `enableHighAccuracy: true`
  - `distanceInterval: 0`
  - Background location permission requested
- Returns `{lat, lng, accuracy, altitude, speed, timestamp}`

### 4.3 Lifecycle Management
```
App Foreground + Trip Active → 50 Hz IMU, 1 Hz GPS
App Background + Trip Active → 50 Hz IMU (where OS permits), background GPS
Trip Inactive / Stationary    → reduce to 5 Hz IMU after 5 min stillness
```

---

## 5. Window Processor

### 5.1 Ring Buffer
- Size: 150 samples
- Stores latest 3 seconds of A_mag values

### 5.2 A_mag Calculation
```typescript
function computeMagnitude(ax: number, ay: number, az: number): number {
  return Math.sqrt(ax * ax + ay * ay + az * az);
}
```

### 5.3 Windowing
- On every 75 new samples (1.5 s), emit a window
- Window payload includes:
  - `traveler_id`
  - `trip_id`
  - `window_index`
  - `timestamp`
  - latest GPS fix
  - `amag: number[]` (150 elements)

### 5.4 Out-of-Range Handling
- If buffer has < 150 samples at window time, pad with mean of available samples or skip.
- If sensor temporarily unavailable, mark window with `sensor_gaps` count.

---

## 6. Offline Queue

### 6.1 SQLite Schema
```sql
CREATE TABLE telemetry_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    traveler_id TEXT NOT NULL,
    trip_id TEXT NOT NULL,
    payload_cipher BLOB NOT NULL,
    iv TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT CHECK(status IN ('PENDING', 'IN_FLIGHT', 'COMMITTED', 'FAILED')) DEFAULT 'PENDING',
    retry_count INTEGER DEFAULT 0
);
```

### 6.2 Encryption
- Algorithm: AES-256-CBC
- Key: session-derived from device-stored secret + trip salt
- IV: 16 random bytes, stored alongside ciphertext

### 6.3 Network Interceptor
```
Before send:
  attempt ping to /health
  if success → send via WebSocket
  if fail    → encrypt payload → insert queue as PENDING
```

### 6.4 Autocommit Job
- Runs every 30 seconds when app is active
- Steps:
  1. Check connectivity.
  2. Select oldest PENDING rows (batch size 50).
  3. Mark IN_FLIGHT.
  4. Send via WebSocket.
  5. On ACK → mark COMMITTED.
  6. On NACK/timeout → increment retry_count, revert to PENDING if < max retries.

---

## 7. Geo-Fence Engine

### 7.1 Data
- GeoJSON `FeatureCollection` of hazard polygons fetched at trip start.
- Cached in SQLite + Redux store.

### 7.2 Evaluation
- On every GPS update:
  - Run `turf.booleanPointInPolygon(point, polygon)` for each cached fence.
  - If entering a hazard zone → local notification + log breach.
  - If inside hazard zone > 10 minutes → escalate to HIGH alert.

### 7.3 Alert UI
- Banner at top of Home screen.
- Push notification even if app in background.

---

## 8. DID Wallet

### 8.1 Key Generation
- Use `ethers.Wallet.createRandom()`.
- Store private key with `SecureStore.setItemAsync('toursafe_private_key', key)`.
- Store public key and address in SecureStore.

### 8.2 Onboarding Registration
1. Generate keypair.
2. Encrypt medical profile JSON with public key → AES-256-GCM symmetric key encrypted by secp256k1.
3. Upload encrypted blob to IPFS via Pinata API.
4. Receive IPFS CID.
5. Call `registerDID(address, publicKeyHash, ipfsCID)` on Polygon Amoy.

### 8.3 QR Code
- Content: JSON string `{did, sig}` where `sig` is a timestamped signature proving key possession.
- Regenerated every 60 seconds to prevent replay attacks.
- Displayed in Profile and Emergency Override screens.

---

## 9. Emergency Override

### 9.1 Manual SOS
- Large button on Home and dedicated Emergency screen.
- Countdown (e.g., 5 seconds) with cancel option to prevent accidental triggers.
- On trigger:
  - Send immediate `SOS_MANUAL` event via WebSocket.
  - Bypass two-stage confirmation.
  - Start high-priority location updates.
  - Show QR code for responder access.

---

## 10. Notifications

### 10.1 Local Notifications
- Geo-fence entry/exit.
- Anomaly confirmation countdown.
- Offline queue flush complete.

### 10.2 Push Notifications
- Requires FCM (Android) and APNS (iOS) setup.
- Backend-initiated alerts for anomalies.

---

## 11. Permissions

| Permission | Android | iOS | Rationale |
|------------|---------|-----|-----------|
| Location foreground | `ACCESS_FINE_LOCATION` | `NSLocationWhenInUseUsageDescription` | Live GPS |
| Location background | `ACCESS_BACKGROUND_LOCATION` | `NSLocationAlwaysAndWhenInUseUsageDescription` | Continuous tracking |
| Activity recognition | `ACTIVITY_RECOGNITION` | `NSMotionUsageDescription` | IMU access |
| Notifications | `POST_NOTIFICATIONS` | `UNUserNotificationCenter` | Alerts |
| Camera | `CAMERA` | `NSCameraUsageDescription` | QR scan by traveler if needed |

---

## 12. State Management

### Redux Slices
- `safetySlice` — current status, anomaly state, geo-fence alerts.
- `connectionSlice` — online/offline, queue length, last sync.
- `tripSlice` — active trip metadata.
- `identitySlice` — DID, public key, QR payload.

### TanStack Query
- Server state: geo-fences, profile sync, incident history.

---

## 13. Error Handling

- All sensor listeners must have try/catch and recovery.
- WebSocket reconnect with exponential backoff (max 30 s).
- SQLite operations wrapped in transactions.
- Graceful degradation if secure enclave unavailable (warn user and disable DID features).

---

## 14. Testing

- Jest + React Native Testing Library for components.
- Detox for E2E flows (onboarding, SOS, offline flush).
- Sensor simulation via mock data files.
- Battery profiling on physical devices.
