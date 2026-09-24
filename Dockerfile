FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    WINEDEBUG=-all \
    DISPLAY=:99 \
    MT5_TERMINAL_PATH=/opt/mt5/terminal64.exe

RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      python3 \
      python3-pip \
      python3-venv \
      xvfb \
      wine64 \
      wine32 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY bridge ./bridge
COPY scripts ./scripts
RUN chmod +x ./scripts/start-mt5.sh

EXPOSE 8000
CMD ["./scripts/start-mt5.sh"]
