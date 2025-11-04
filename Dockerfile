FROM python:3.11-slim

LABEL authors="IvanGomezDellOsa"

LABEL maintainer="FreeMagicMirror"
LABEL description="FreeMagicMirror - Smart mirror photo booth built with Kivy and OpenCV"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libgles2 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY config.py main.py /app/
COPY screens /app/screens
COPY assets /app/assets

RUN pip install --no-cache-dir \
    kivy==2.3.1 \
    opencv-python==4.10.0.84 \
    ffpyplayer==4.5.3 \
    screeninfo==0.8.1

RUN mkdir -p /app/gallery

# Command to start the app
CMD ["python", "main.py"]