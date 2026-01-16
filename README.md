# human_ml_mask_api_parser

[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Compose](https://img.shields.io/badge/Compose-supported-384D54?logo=docker&logoColor=white)](./docker-compose.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](./pyproject.toml)
[![Pytorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./schp/LICENSE)
[![Issues](https://img.shields.io/github/issues/your-org-or-user/human_ml_mask_api_parser.svg)](./)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./)
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)](./)

A service for generating binary human/clothing masks on top of images based on human parsing models (SCHP / CE2P and related modules). It exposes a simple HTTP API and optional CLI for batch processing.

- Quick start via Docker/Compose
- Local run with Python (pyproject + uv)
- Built-in models and demo assets (schp/demo)
- Configurable parser: choose mask type, pre/post-processing

TIP: The service is currently configured to produce a clothing mask. You can change this in the parser settings (see app/parser.py) by selecting the mask type/classes that fit your use case.

## Table of Contents
- About
- Architecture
- Requirements
- Quick Start
- Local Installation
- Run the Service
- HTTP API
- Image Processing (CLI)
- Configuration and Mask Modes
- Test Data
- Development
- License

## About
This repository wraps human parsing models into a convenient service for extracting regions of interest on a person — in the default configuration it generates a clothing mask. Class selection and post-processing live in app/parser.py, while the HTTP layer lives in app/main.py.

Key directories:
- app/ — service entry point and mask parser logic
- schp/ — SCHP/CE2P models/utilities (and extensions)
- Dockerfile, docker-compose.yml — containerization
- pyproject.toml, uv.lock — dependency management

## Architecture
- Models: SCHP/CE2P and helper modules under schp/
- API: lightweight Python web app (see app/main.py)
- Parser: single configuration point for mask classes/modes (app/parser.py)

## Requirements
- Python 3.10+
- macOS/Linux (x86_64). GPU acceleration optional (CUDA if available)
- Docker (optional) and docker-compose for containerized runs

## Quick Start
The fastest way is Docker Compose:

1) Build and run
   docker-compose up --build

2) Check
   - The service will be available at http://localhost:8000

Stop
   docker-compose down

Alternative (local, without Docker):
   chmod +x setup.sh && ./setup.sh
   uv run python -m app.main

## Local Installation
Local setup without Docker using the provided setup script.

1) Make the script executable (once):
   chmod +x setup.sh

2) Run the setup:
   ./setup.sh

This script installs dependencies, prepares the environment and downloads required assets (if applicable).

## Run the Service
- Locally (via uv):
  uv run python -m app.main
  By default the server listens on http://0.0.0.0:8000

- Via Docker directly:
  docker build -t human-ml-mask-api-parser:latest .
  docker run --rm -p 8000:8000 human-ml-mask-api-parser:latest

- Via Makefile (if configured):
  make run

## Configuration and Mask Modes
The main logic for selecting the mask type is in app/parser.py. There you can:
- pick predefined segmentation classes (e.g., clothes-only, hair, skin, full body)
- tune post-processing (morphology, smoothing, NMS for instances, etc.)
- adjust thresholds, color channels, model input size

TIP: The default mode is "clothing mask". To switch modes, open app/parser.py and change the configuration for the class/classes used to compose the final mask.

## Test Data
The schp/demo/ directory contains example images to quickly verify the pipeline. You can send demo.jpg to the /mask endpoint or use the local command if provided.

## Development
- Code style: follow the project's existing formatting
- Dependencies: pyproject.toml + uv.lock
- Tests: add smoke tests for basic scenarios (health, single /mask run)
- Performance: when a GPU is available, verify the models use CUDA correctly

Useful commands:
- Docker build: docker build -t human-ml-mask-api-parser:latest .
- Local setup: chmod +x setup.sh && ./setup.sh
- Local run: uv run python -m app.main
- Compose: docker-compose up --build

## License
See schp/LICENSE for licenses of models and code within schp/. For production usage, ensure license compliance with your policies.
