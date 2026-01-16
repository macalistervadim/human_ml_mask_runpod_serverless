#!/bin/bash
set -e

MAIN_REPO="https://github.com/macalistervadim/human_ml_mask_api_parser.git"
MODEL_ID="1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP"
MODEL_NAME="exp-schp-201908301523-atr.pth"


echo "Initializing and updating submodules..."
git submodule update --init --recursive

echo "Downloading ATR model..."
MODEL_PATH="schp/$MODEL_NAME"

if [ ! -f "$MODEL_PATH" ]; then
    pip install --quiet gdown

    gdown --id $MODEL_ID -O "$MODEL_PATH"
else
    echo "Model already exists, skipping download."
fi


echo "Starting project with Docker..."
make up

echo "✅ Setup complete! FastAPI should be available at http://localhost:8000"
