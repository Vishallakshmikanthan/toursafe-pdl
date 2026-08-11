# 07 — Blockchain / DID Specification

> Specification for TourSafe's Self-Sovereign Identity layer anchored on Polygon PoS.

---

## 1. Design Principles

1. **Self-Sovereign Identity (SSI)**: Traveler owns and controls identity credentials.
2. **Privacy by Design**: Medical data never stored on-chain; only DID hash and encrypted vault CID are public.
3. **Emergency-Only Decryption**: Agencies can decrypt only after AI-confirmed emergency.
4. **Immutable Audit Trail**: Every access grant is recorded on-chain.

---

## 2. Standards

- **W3C Decentralized Identifiers (DIDs)** v1.0
- **Verifiable Credentials** data model (future consideration)
- **ERC-712** typed data signing for QR tokens
- **secp256k1** elliptic curve cryptography

---

## 3. Networks

| Environment | Network | Chain ID | Purpose |
|-------------|---------|----------|---------|
| Local dev | Hardhat Network | 31337 | Rapid iteration |
| Testnet | Polygon Amoy | 80002 | Integration testing |
| Production | Polygon PoS Mainnet | 137 | Live deployment |

---

## 4. Identity Resolution Contract

### Contract: `IdentityResolution.sol`

### Data Structures
```solidity
struct DIDRecord {
    bytes32 publicKeyHash;
    string ipfsCID;
    uint256 registeredAt;
    bool active;
}

struct EmergencyAccess {
    address agency;
    uint256 grantedAt;
    uint256 expiresAt;
    bool active;
}

mapping(address => DIDRecord) public dids;
mapping(address => EmergencyAccess[]) public emergencyAccesses;

address public admin;
mapping(address => bool) public authorizedAgencies;
```

### Events
```solidity
event DIDRegistered(address indexed traveler, bytes32 publicKeyHash, string ipfsCID);
event EmergencyAccessGranted(address indexed traveler, address indexed agency, uint256 expiresAt);
event EmergencyAccessRevoked(address indexed traveler, address indexed agency);
event AgencyAuthorized(address indexed agency);
event AgencyRevoked(address indexed agency);
```

### Functions

#### `registerDID`
```solidity
function registerDID(
    bytes32 _publicKeyHash,
    string calldata _ipfsCID
) external;
```
- Called by traveler during onboarding.
- Stores public key hash and IPFS CID.
- Emits `DIDRegistered`.

#### `resolveDID`
```solidity
function resolveDID(address _traveler)
    external
    view
    returns (bytes32 publicKeyHash, string memory ipfsCID, uint256 registeredAt);
```
- Called by anyone to read public metadata.

#### `grantEmergencyAccess`
```solidity
function grantEmergencyAccess(address _traveler, address _agency) external onlyAdmin;
```
- Called by TourSafe backend after AI-confirmed anomaly.
- `_agency` must be pre-authorized.
- Access expires after 24 hours by default.
- Emits `EmergencyAccessGranted`.

#### `revokeEmergencyAccess`
```solidity
function revokeEmergencyAccess(address _traveler, address _agency) external onlyAdmin;
```
- Called when emergency is resolved.

#### `checkEmergencyAccess`
```solidity
function checkEmergencyAccess(address _traveler, address _agency)
    external
    view
    returns (bool);
```
- Returns true if active, non-expired access exists.

#### Agency Management
```solidity
function authorizeAgency(address _agency) external onlyAdmin;
function revokeAgency(address _agency) external onlyAdmin;
```

---

## 5. Key Management

### Traveler Keypair
- Generated in mobile app via `ethers.Wallet.createRandom()`.
- Private key stored in device secure enclave (Expo SecureStore / iOS Keychain).
- Public key submitted to smart contract as hash.

### Agency Emergency Cryptographic Access Key
- Generated off-chain by TourSafe admin for each registered agency.
- Distributed securely to agency dashboard backend (never hardcoded in frontend).
- Used to decrypt the symmetric key that encrypts the IPFS vault.

---

## 6. Encrypted Medical Vault

### Vault Content
```json
{
  "name": "John Doe",
  "date_of_birth": "1990-01-01",
  "blood_type": "O+",
  "allergies": ["penicillin", "peanuts"],
  "medical_conditions": ["asthma"],
  "medications": ["salbutamol"],
  "emergency_contacts": [
    {"name": "Jane Doe", "phone": "+91-...", "relationship": "spouse"}
  ],
  "insurance_policy": "...",
  "home_country": "India",
  "passport_nationality": "..."
}
```

### Encryption Flow
1. Generate random AES-256-GCM key `K`.
2. Encrypt vault JSON with `K` → ciphertext + auth tag.
3. Encrypt `K` with traveler's secp256k1 public key using ECIES.
4. Bundle encrypted key + ciphertext + IV + tag.
5. Upload to IPFS → receive CID.
6. Store CID in smart contract.

### Decryption Flow (Emergency)
1. Agency backend calls `grantEmergencyAccess(traveler, agency)`.
2. Fetch encrypted vault from IPFS using CID.
3. Agency uses its Emergency Cryptographic Access Key to decrypt `K`.
4. Decrypt vault JSON with `K`.
5. Display to authorized responder.

> Note: Exact key-escrow mechanism (traveler key vs agency key vs threshold scheme) is a design decision to be finalized before mainnet. Minimum viable approach: vault encrypted with traveler public key and a backup agency public key, both stored in the bundle.

---

## 7. QR Code Protocol

### QR Payload
```json
{
  "did": "did:polygon:0x...",
  "timestamp": 1691234567,
  "signature": "0x..."
}
```

### Signature
- Sign `keccak256(did + timestamp)` with traveler private key.
- Prevents replay attacks via timestamp expiry (e.g., 120 seconds).

### Responder Verification
1. Verify signature against DID public key.
2. Check timestamp within expiry window.
3. Resolve DID on-chain.
4. Proceed to vault decryption if emergency access active.

---

## 8. Deployment Pipeline

### Hardhat Setup
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat test
```

### Local Deployment
```bash
npx hardhat node
npx hardhat run scripts/deploy.ts --network localhost
```

### Testnet Deployment
```bash
npx hardhat run scripts/deploy.ts --network amoy
npx hardhat verify --network amoy DEPLOYED_CONTRACT_ADDRESS
```

### Mainnet Deployment
- Requires third-party security audit.
- Multi-sig admin wallet recommended.
- Gas budget prepared and monitored.

---

## 9. Security Considerations

- Never store private keys in code or Git.
- Use environment variables or secure secret managers.
- Admin key must be multi-sig or hardware wallet in production.
- All access events logged on-chain.
- Smart contract upgrade strategy: deploy new contract and migrate; contracts are non-upgradeable unless explicitly designed as proxy.

---

## 10. Testing

- Unit tests for every contract function.
- Access control tests (only admin can grant access).
- Event emission tests.
- Integration test: register DID → grant access → resolve → revoke.
- Testnet end-to-end with real IPFS upload.
