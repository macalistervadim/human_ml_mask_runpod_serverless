#!/bin/bash
set -e

# Настройки
MAIN_REPO="https://github.com/macalistervadim/human_ml_mask_api_parser.git"

echo "1️⃣ Cloning main repository..."
git clone "$MAIN_REPO"
cd human_ml_mask_api_parser

echo "2️⃣ Initializing and updating submodules..."
git submodule update --init --recursive

echo "3️⃣ Starting the project with Docker..."
make up

echo "✅ Project is running! FastAPI should be available at http://localhost:8000"
