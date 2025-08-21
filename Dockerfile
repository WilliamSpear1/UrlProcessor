# =========================
# 1. Builder stage
# =========================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install only what’s needed to build wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ build-essential \
    python3-dev libffi-dev libssl-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and build wheels for your deps
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# =========================
# 2. Runtime stage
# =========================
FROM python:3.12-slim

WORKDIR /app

# Install lightweight runtime deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget less \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome (headless for Selenium, etc.)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Copy prebuilt wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy project source
COPY . /app

EXPOSE 5001

# Run Gunicorn (serving Flask app)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "wsgi:app"]
