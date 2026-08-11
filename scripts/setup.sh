#!/usr/bin/env bash
set -e

echo "Setting up TourSafe development environment..."

# Backend
cd backend
python -m venv .venv || true
source .venv/bin/activate
pip install -r requirements.txt
cd ..

# Mobile
cd mobile
npm install
cd ..

# Dashboard
cd dashboard/client
npm install
cd ../server
npm install
cd ../..

# Blockchain
cd blockchain
npm install
cd ..

# Config
cp config/.env.example config/.env

echo "Setup complete. Edit config/.env with your secrets."
