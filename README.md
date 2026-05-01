# UrlProcessor

A distributed web scraping application that extracts and downloads video URLs from web pages using Selenium and asynchronous task processing with Celery.

## Prerequisites
- **Python3.11**
- **Docker & Docker Compose**
- **Redis**
- **Selenium + SeleniumWire**
- **Celery**

## Installation
1. Create a virtual environment
  - python3.12 -m venv .venv
  - source .vevn/bin/activate # On Windows
2. Install dependencies
  - pip install -r requirements.txt
3. cp env.exmaple .env
4. docker run -d -p 6379:6379 redis:latest
5.
    - python -m flask --app src.api run --host 0.0.0.0 --port 5000
    - celery -A src.configuration.celery_app worker -Q url_process_queue -l info

## Docker Deployment
1. docker network create app-net
2. cp env.example .env
3. docker-compose build
4. docker-compose up -d
5. docker-compose logs -f url_processor
6. docker-compose logs -f celery_worker_url_processor