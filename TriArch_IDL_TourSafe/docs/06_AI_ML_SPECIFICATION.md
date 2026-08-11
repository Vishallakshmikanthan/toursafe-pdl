# 06 — AI / ML Specification

> Specification for the TourSafe anomaly detection engine: LSTM Autoencoder, data processing, training, inference, and evaluation.

---

## 1. Objective

Autonomously detect emergencies — crashes and immobility/unconsciousness events — from mobile IMU sensor streams, without requiring labeled emergency training data.

---

## 2. Why Anomaly Detection?

Collecting real-world crash and unconsciousness data from travelers is:
- Ethically impossible.
- Statistically rare.
- Jurisdictionally complex.

Instead, train a model exclusively on **normal activity**. Any deviation from normal patterns produces high reconstruction error, signaling an anomaly.

---

## 3. Input Data

### Raw Sensor Stream
- 3-axis accelerometer: `Ax, Ay, Az` (m/s²)
- Sampling rate: 50 Hz
- GPS: lat, lng, accuracy (1 Hz)

### Orientation-Invariant Feature
To make the model robust to phone orientation and placement, transform raw axes into total acceleration magnitude:

```
A_mag = sqrt(Ax² + Ay² + Az²)
```

Properties:
- Independent of device orientation.
- Captures overall motion intensity.
- Earth gravity baseline ≈ 9.81 m/s² when stationary.

### Windowing
- Window length: 150 samples (3 seconds)
- Slide: 75 samples (1.5 seconds)
- Overlap: 50%
- Input shape to model: `(batch_size, 150, 1)`

---

## 4. Model Architecture

### Sequence-to-Sequence LSTM Autoencoder

```
Input (150, 1)
    ↓
LSTM(64, return_sequences=True)
    ↓
LSTM(32, return_sequences=False)
    ↓
Latent vector (32)
    ↓
RepeatVector(150)
    ↓
LSTM(32, return_sequences=True)
    ↓
LSTM(64, return_sequences=True)
    ↓
TimeDistributed(Dense(1))
    ↓
Output (150, 1)
```

### Loss Function
- Mean Squared Error (MSE) between input window and reconstructed window.

### Optimizer
- Adam with default learning rate 0.001.

### Training Data
- Normal activities only:
  - Walking
  - Running
  - Sitting / standing
  - Driving (car, bus)
  - Light hiking
  - Phone in pocket, hand, bag

---

## 5. Anomaly Detection Logic

### Reconstruction Error
For each window:
```
error = mean((input_window - reconstructed_window)²)
```

### Threshold Calibration
1. Run model on held-out validation set of normal data.
2. Compute reconstruction errors.
3. Set threshold at 99.5th percentile.
- Expected false positive: ~0.5% of windows.
- At 1 window per 1.5 s, roughly 1 false positive per 5 minutes of monitoring.

### Two-Stage Confirmation
- Stage 1: single window exceeds threshold → first-stage flag.
- Stage 2: next overlapping window also exceeds threshold → confirmed anomaly.
- Single-window noise spikes are filtered out.

---

## 6. Twin Trigger Scenarios

### 6.1 Crash / Physical Impact
Signature:
- Massive instantaneous A_mag spike (high G-force).
- Followed by either:
  - Chaotic, disorganized motion (tumbling), or
  - Abrupt cessation of motion.

Confirmation:
- LSTM reconstruction error >> threshold for two consecutive windows.

### 6.2 Immobility / Unconsciousness
Signature:
- A_mag flatline at approximately 9.81 m/s² for multiple windows.
- GPS coordinate static.
- Location is in remote / isolated zone (not a known rest area).

Confirmation:
- LSTM error elevated due to unnatural stillness context.
- GPS static for > configurable duration (default 5 minutes).
- Server-side check against geo-fence / safety-zone data.

---

## 7. SNN-CAD — Spatial Trajectory Anomaly (Conceptual / Stretch)

### Concept
Sequential Nearest Neighbor Cumulative Anomaly Detection (SNN-CAD) compares recent GPS trajectory to historical safe routes for the same area.

### Metric
Hausdorff distance between observed trajectory and nearest safe route.

### Use
- Predictive hazard alert before an accident occurs.
- Independent signal that can raise alert level to amber.

### Target AUC
≥ 0.97 on labeled trajectory datasets.

### Status
Conceptual for MVP; implement only if time permits after core LSTM pipeline is validated.

---

## 8. Training Pipeline

### Data Collection
| Source | Description |
|--------|-------------|
| Mobile recordings | Team members collect labeled normal activity sessions. |
| Public datasets | HAR (Human Activity Recognition) datasets with accelerometer data. |
| Synthetic augmentation | Add noise, simulate phone orientations. |

### Preprocessing
1. Load raw Ax, Ay, Az.
2. Compute A_mag.
3. Segment into 150-point windows with 50% overlap.
4. Split: 70% train / 15% validation / 15% test.
5. Optional z-score normalization using training statistics.

### Training Script
```python
# ml/train.py pseudo-code
model = build_lstm_autoencoder()
model.compile(optimizer='adam', loss='mse')
history = model.fit(train_windows, train_windows,
                    validation_data=(val_windows, val_windows),
                    epochs=100,
                    batch_size=64,
                    callbacks=[EarlyStopping(patience=10),
                               ModelCheckpoint('best_model.keras')])
```

### Hyperparameters
| Parameter | Value |
|-----------|-------|
| LSTM units (encoder) | 64, 32 |
| LSTM units (decoder) | 32, 64 |
| Latent dim | 32 |
| Batch size | 64 |
| Learning rate | 0.001 |
| Early stopping patience | 10 |

---

## 9. ONNX Export & Inference

### Export
```bash
python -m tf2onnx.convert \
  --saved-model ./models/lstm_saved_model \
  --output ./models/lstm_autoencoder.onnx
```

### Validation
- Compare TensorFlow and ONNX outputs on same windows.
- Max absolute difference must be < 1e-5.

### Runtime
```python
import onnxruntime as ort
session = ort.InferenceSession("lstm_autoencoder.onnx",
                              providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
reconstructed = session.run(None, {input_name: window})[0]
error = np.mean((window - reconstructed) ** 2)
```

---

## 10. Evaluation Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Inference latency | < 100 ms | Per window on CPU |
| False positive rate | < 2% | After two-stage confirmation |
| Recall on simulated crash | > 95% | High-G impulse tests |
| Recall on simulated immobility | > 90% | Static device in remote zone |
| AUC (SNN-CAD) | > 0.97 | If implemented |

---

## 11. Dataset Requirements

### Normal Activity Dataset
- Minimum 10 hours of diverse normal activity.
- Multiple phone placements: pocket, hand, bag, mount.
- Multiple transport modes.

### Anomaly Test Dataset
- Simulated crashes: drop phone, shake vigorously.
- Simulated immobility: phone placed stationary on desk.
- Must not be used during training.

### Dataset Storage
- Store in `ml/data/raw/`, `ml/data/processed/`, `ml/data/test/`.
- Use `.csv` or `.parquet` format.
- Never commit large datasets to Git; use DVC or cloud storage.

---

## 12. Retraining Policy

- Retrain model when:
  - False positive rate in production exceeds 2%.
  - New activity patterns are observed (e.g., new transport modes).
  - Quarterly scheduled review.
- Use only anonymized, aggregated archived telemetry.
- Document each retraining run in `ml/experiments/`.
