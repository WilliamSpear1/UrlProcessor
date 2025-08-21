FROM python:3.11-slim

WORKDIR /app

# Install system dependencies first
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        build-essential \
        wget \
        curl \
        python3-dev \
        libffi-dev \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        less && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip and install requirements
RUN pip install --upgrade pip setuptools wheel && \
    pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "URLProcessor:app"]