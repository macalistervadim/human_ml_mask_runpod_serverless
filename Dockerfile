FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    ffmpeg \
    libsm6 \
    libxext6 \
    tzdata \
    && rm -rf /var/lib/apt/lists/*


COPY app/ ./app/
COPY schp/ ./schp/
COPY pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock

RUN pip install --no-cache-dir \
    Pillow \
    numpy \
    opencv-python \
    tqdm \
    runpod \
    torch==2.1.0 \
    torchvision==0.16.0 \
    gdown \
    Brotli \
    httpx[http2]

RUN gdown --id 1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP \
    -O /app/schp/exp-schp-201908301523-atr.pth

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "app/handler.py"]
