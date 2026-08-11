# TourSafe

> AI-Driven Emergency Response & Blockchain Identity Infrastructure for Travelers.

## Quick Start

1. Read [docs/00_MASTER_CONTEXT.md](TriArch_IDL_TourSafe/docs/00_MASTER_CONTEXT.md).
2. Follow [docs/20_EXECUTION_PLAYBOOK.md](TriArch_IDL_TourSafe/docs/20_EXECUTION_PLAYBOOK.md) to set up the environment.
3. See domain specs in [docs/](TriArch_IDL_TourSafe/docs/) for module details.

## Repository Structure

- `mobile/` — React Native + TypeScript traveler app.
- `backend/` — FastAPI real-time telemetry and ML inference.
- `ml/` — LSTM Autoencoder training, ONNX export, datasets.
- `blockchain/` — Solidity DID contracts + Hardhat.
- `dashboard/` — MERN authority dashboard + Mapbox.
- `hardware/` — ESP32 / Raspberry Pi Pico W prototype.
- `tests/` — Cross-module integration and load tests.
- `scripts/` — Setup and seed helpers.
- `config/` — Docker Compose and Nginx configuration.
- `docs/` — Engineering implementation documentation.
- `TriArch_IDL_TourSafe/docs/` — Original project/reference documentation.

## Team

- Member 1 — Backend + Architecture + DevOps
- Member 2 — Mobile + AI/ML + Blockchain
- Member 3 — UI Support + Testing + Documentation + Datasets

## License

TBD — see institution guidelines.
