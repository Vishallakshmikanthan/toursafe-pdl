# 20 — Execution Playbook

> Step-by-step instructions to set up the TourSafe development environment and run the system.

---

## 1. Prerequisites

- Windows / macOS / Linux
- Git
- Node.js 20 LTS
- Python 3.11+
- Docker + Docker Compose
- Android Studio (for Android emulator)
- Xcode (for iOS, macOS only)
- MetaMask or similar wallet
- Polygon Amoy test MATIC (from faucet)

---

## 2. Clone and Setup

```bash
git clone <repo-url>
cd TourSafe
```

### Create environment files
```bash
cp config/.env.example config/.env
cp mobile/.env.example mobile/.env
cp backend/.env.example backend/.env
cp dashboard/server/.env.example dashboard/server/.env
cp blockchain/.env.example blockchain/.env
```

Fill in all required values (RPC URLs, keys, tokens).

---

## 3. Start Backend with Docker Compose

```bash
docker compose -f config/docker-compose.dev.yml up --build
```

This starts:
- FastAPI on `http://localhost:8000`
- MongoDB on `localhost:27017`
- Redis on `localhost:6379`
- Dashboard Node server on `http://localhost:4000`
- Dashboard React app on `http://localhost:5173`

---

## 4. Run Backend Locally (Optional)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 5. Run Mobile App

### Android
```bash
cd mobile
npm install
npx react-native start
npx react-native run-android
```

### iOS
```bash
cd mobile
npm install
cd ios && pod install && cd ..
npx react-native run-ios
```

---

## 6. Run Dashboard

```bash
cd dashboard/client
npm install
npm run dev

cd dashboard/server
npm install
npm run dev
```

---

## 7. Deploy Smart Contracts

### Local
```bash
cd blockchain
npx hardhat node
npx hardhat run scripts/deploy.ts --network localhost
```

### Amoy Testnet
```bash
npx hardhat run scripts/deploy.ts --network amoy
```

Update contract address in backend and dashboard `.env` files.

---

## 8. Seed Demo Data

```bash
python scripts/seed_demo.py
```

This creates:
- Demo travelers
- Demo geo-fences
- Demo emergency resources
- Demo agency accounts

---

## 9. Run Tests

### Backend
```bash
cd backend
pytest
```

### Mobile
```bash
cd mobile
npm test
```

### Blockchain
```bash
cd blockchain
npx hardhat test
```

### Dashboard
```bash
cd dashboard/server
npm test
```

---

## 10. Run Load Tests

```bash
cd tests/load
locust -f locustfile.py
```

Open `http://localhost:8089` and configure user count.

---

## 11. Hardware Prototype

### Flash ESP32
```bash
cd hardware/esp32
pio run --target upload
```

### Monitor Serial
```bash
pio device monitor
```

---

## 12. Troubleshooting

| Issue | Fix |
|-------|-----|
| Metro bundler fails | Clear cache: `npx react-native start --reset-cache` |
| MongoDB connection refused | Ensure Docker Compose is running |
| WebSocket disconnects | Check firewall; verify WS URL |
| Hardhat deploy fails | Verify private key has Amoy MATIC |
| ONNX inference slow | Reduce worker count or use GPU provider |
| Android emulator slow | Enable HAXM / Hyper-V; use physical device |

---

## 13. Daily Workflow

1. Pull latest `main`.
2. Start Docker Compose.
3. Work on assigned module.
4. Write/update tests.
5. Run relevant test suite.
6. Update `25_CURRENT_STATE.md` if status changes.
7. Commit to feature branch.
8. Open PR for review.
