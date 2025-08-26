# =========================
# 1. Builder stage
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ build-essential \
    python3-dev libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and pre-build wheels for dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# =========================
# 2. Runtime stage
# =========================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies (no heavy build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget less \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Copy prebuilt wheels from builder
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy project code
COPY . /app

EXPOSE 5001

CMD ["gunicorn","app:app", \
    "--bind", "0.0.0.0:5001", \
    "--workers", "4", \
    "--worker-class", "gthread", \
    "--threads", "2", \
    "--timeout", "120", \
    "--max-requests", "1000", \
    "--max-requests-jitter", "50", \
    "--log-level", "info", \
    "--error-logfile", "-", \
    "--access-logfile", "-", \
    "--capture-output"]