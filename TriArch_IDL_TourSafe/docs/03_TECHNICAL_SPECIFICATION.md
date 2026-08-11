# 03 — Technical Specification

> Concrete technical standards, data formats, libraries, and environment requirements for TourSafe.

---

## 1. Development Environment

### Required Tools
| Tool | Purpose | Version |
|------|---------|---------|
| Node.js | Mobile + dashboard runtime | LTS 20.x |
| Python | Backend + ML | 3.11+ |
| React Native CLI | Mobile framework | 0.74+ |
| FastAPI | Backend framework | 0.111+ |
| TensorFlow | ML training | 2.16+ |
| Hardhat | Smart contract dev | 2.22+ |
| Docker | Containerization | 24.x+ |
| Docker Compose | Local orchestration | 2.24+ |
| Git | Version control | 2.42+ |
| VS Code | Primary IDE | latest |
| Android Studio | Android emulation | latest |

### Recommended VS Code Extensions
- Python
- Pylance
- ESLint
- Prettier
- Solidity
- Docker
- GitLens
- GitHub Copilot

---

## 2. Mobile Technical Spec

### Framework & Language
- React Native CLI (bare workflow)
- TypeScript 5.x
- Hermes engine enabled

### Core Libraries
| Library | Purpose |
|---------|---------|
| `react-native` | Framework |
| `@reduxjs/toolkit` + `react-redux` | Global state |
| `@tanstack/react-query` | Server state sync |
| `react-native-sensors` or Expo Sensors | IMU access |
| `expo-location` | Background GPS |
| `react-native-sqlite-storage` | Offline queue |
| `@react-native-async-storage/async-storage` | Session state |
| `react-native-keychain` / Expo SecureStore | Private key storage |
| `ethers` | Blockchain interactions |
| `react-native-qrcode-svg` | QR display |
| `@turf/turf` | Geo-fence checks |
| `react-native-maps` | Map rendering |
| `axios` | HTTP calls |

### Sensor Configuration
| Sensor | Rate | Data |
|--------|------|------|
| Accelerometer | 50 Hz | Ax, Ay, Az (m/s²) |
| GPS | 1 Hz | lat, lng, accuracy, speed, timestamp |

### Window Spec
- Length: 150 samples (3 seconds at 50 Hz)
- Slide: 75 samples (1.5 seconds, 50% overlap)
- Feature: `A_mag = sqrt(Ax² + Ay² + Az²)`
- Output: 150-element float array

---

## 3. Backend Technical Spec

### Framework
- FastAPI 0.111+
- Uvicorn ASGI server
- Python 3.11+

### Core Libraries
| Library | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn[standard]` | ASGI server |
| `pydantic` | Data validation |
| `websockets` | WebSocket support |
| `python-socketio` | Socket.io server |
| `motor` | Async MongoDB driver |
| `redis[asyncio]` | Async Redis client |
| `onnxruntime` | ML inference |
| `numpy` | Numerical processing |
| `cryptography` | AES operations |
| `httpx` | Async HTTP client |
| `pytest` + `pytest-asyncio` | Testing |

### WebSocket Protocol
- Endpoint: `/ws/telemetry/{traveler_id}`
- Message format: JSON
- Heartbeat: every 30 seconds
- Reconnect: exponential backoff on client

### REST Endpoints (v1)
| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/travelers` | Register traveler |
| GET | `/api/v1/travelers/{id}` | Get traveler profile |
| GET | `/api/v1/geo-fences` | Get active geo-fences |
| GET | `/api/v1/incidents` | List incidents |
| GET | `/api/v1/incidents/{id}` | Get incident details |
| POST | `/api/v1/incidents/{id}/confirm` | Operator confirms dispatch |

---

## 4. ML Technical Spec

### Model Architecture
- Sequence-to-Sequence LSTM Autoencoder
- Input: `(batch, 150, 1)` float32
- Encoder:
  - LSTM(64, return_sequences=True)
  - LSTM(32, return_sequences=False)
- Latent: 32-dim repeat vector
- Decoder:
  - RepeatVector(150)
  - LSTM(32, return_sequences=True)
  - LSTM(64, return_sequences=True)
  - TimeDistributed(Dense(1))
- Loss: Mean Squared Error
- Optimizer: Adam (learning_rate=0.001)

### Training
- Dataset: hours of normal activity A_mag sequences
- Batch size: 64
- Epochs: 50–100 with early stopping
- Validation split: 20%
- Threshold: 99.5th percentile validation reconstruction error

### Inference
- Runtime: ONNX Runtime
- Target latency: < 100 ms per window
- Worker pool: 4 async workers minimum

### Export
```python
# tf2onnx example
python -m tf2onnx.convert --saved-model ./lstm_model --output ./lstm_autoencoder.onnx
```

---

## 5. Blockchain Technical Spec

### Network
- Development: Hardhat local node
- Testing: Polygon Amoy Testnet (Chain ID 80002)
- Production: Polygon PoS Mainnet

### Smart Contract
- Language: Solidity ^0.8.20
- Framework: Hardhat with TypeScript
- Contract: `IdentityResolution.sol`

### Key Functions
```solidity
function registerDID(
    address traveler,
    bytes32 publicKeyHash,
    string calldata ipfsCID
) external;

function resolveDID(address traveler)
    external
    view
    returns (bytes32 publicKeyHash, string memory ipfsCID, uint256 registeredAt);

function grantEmergencyAccess(address traveler, address agency) external;
function revokeEmergencyAccess(address traveler, address agency) external;
```

### Cryptography
- Key pair: secp256k1
- Vault encryption: ECIES or RSA-OAEP over AES-256-GCM
- Offline queue encryption: AES-256-CBC with session-derived key

---

## 6. Dashboard Technical Spec

### Frontend
- React 18 + TypeScript
- Vite build tool
- Mapbox GL JS for maps
- Tailwind CSS for styling
- Socket.io-client for realtime

### Backend Microservices
- Node.js 20 + Express.js
- MongoDB native driver or Mongoose
- Socket.io server
- Puppeteer or pdf-lib for PDF generation

### Pages
- `/login` — agency authentication
- `/map` — live traveler map
- `/incidents` — incident feed
- `/travelers` — directory
- `/efir` — e-FIR archive
- `/qr-scan` — responder QR scanner

---

## 7. Data Formats

### Telemetry Window Payload
```json
{
  "traveler_id": "uuid-string",
  "trip_id": "uuid-string",
  "timestamp": "2026-08-11T12:34:56.789Z",
  "window_index": 42,
  "gps": {
    "lat": 12.3456,
    "lng": 78.9012,
    "accuracy": 4.5
  },
  "amag": [9.81, 9.82, 9.80, "... 150 floats"]
}
```

### Incident Packet
```json
{
  "incident_id": "uuid-string",
  "traveler_id": "uuid-string",
  "trip_id": "uuid-string",
  "event_type": "CRASH | IMMOBILITY | GEOFENCE_BREACH",
  "severity": "CRITICAL | HIGH | MEDIUM",
  "timestamp": "2026-08-11T12:34:56.789Z",
  "gps": {"lat": 12.3456, "lng": 78.9012},
  "reconstruction_error": 0.045,
  "threshold": 0.012,
  "lstm_window": ["...150 floats"],
  "offline_data_flag": false,
  "geo_fence_status": []
}
```

### e-FIR Payload
```json
{
  "incident_id": "uuid-string",
  "generated_at": "2026-08-11T12:35:00.000Z",
  "traveler": {
    "did": "did:polygon:...",
    "name": "...",
    "blood_type": "O+",
    "allergies": ["penicillin"],
    "conditions": ["diabetes"],
    "emergency_contacts": [{"name": "...", "phone": "...", "relation": "..."}]
  },
  "incident": { "timestamp": "...", "gps": {...}, "type": "...", "error": 0.045 },
  "dispatch_targets": {
    "police": {"name": "...", "distance_km": 2.3, "api_endpoint": "..."},
    "hospital": {"name": "...", "distance_km": 4.1, "api_endpoint": "..."}
  }
}
```

---

## 8. Environment Variables

### Mobile
```env
API_BASE_URL=https://api.toursafe.example
WS_URL=wss://api.toursafe.example
POLYGON_RPC_URL=https://polygon-amoy.g.alchemy.com/v2/...
IPFS_GATEWAY=https://gateway.pinata.cloud/ipfs/
```

### Backend
```env
APP_ENV=development
MONGODB_URI=mongodb://localhost:27017/toursafe
REDIS_URL=redis://localhost:6379/0
WS_HEARTBEAT_INTERVAL=30
ONNX_MODEL_PATH=/app/models/lstm_autoencoder.onnx
ANOMALY_THRESHOLD=0.012
POLYGON_RPC_URL=https://polygon-amoy.g.alchemy.com/v2/...
CONTRACT_ADDRESS=0x...
```

### Dashboard
```env
REACT_APP_API_URL=https://api.toursafe.example
REACT_APP_SOCKET_URL=https://api.toursafe.example
REACT_APP_MAPBOX_TOKEN=...
JWT_SECRET=...
POLYGON_RPC_URL=...
CONTRACT_ADDRESS=...
AGENCY_PRIVATE_KEY=...
```

---

## 9. Build & Run Commands

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Mobile
```bash
cd mobile
npm install
npx react-native run-android
# or
npx react-native run-ios
```

### Dashboard
```bash
cd dashboard/client
npm install && npm run dev
cd dashboard/server
npm install && npm run dev
```

### Blockchain
```bash
cd blockchain
npm install
npx hardhat test
npx hardhat run scripts/deploy.ts --network amoy
```

### Full Dev Stack
```bash
docker compose -f config/docker-compose.dev.yml up --build
```
