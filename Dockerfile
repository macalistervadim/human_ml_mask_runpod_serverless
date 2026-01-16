FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime


RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY app/ ./app/
COPY main.py ./main.py
COPY pyproject.toml ./pyproject.toml
COPY uv.lock ./uv.lock

COPY schp/ /schp

RUN pip install --no-cache-dir fastapi uvicorn python-multipart Pillow numpy opencv-python


RUN pip install --no-cache-dir torch==1.5.1 torchvision==0.6.1 tqdm==4.55.0


ADD schp/exp-schp-201908301523-atr.pth /schp/exp-schp-201908301523-atr.pth

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
