# Scraper Dockerfile
FROM python:3.10-slim

WORKDIR /app

# System dependencies (including Chrome for Selenium)
RUN apt-get update && apt-get install -y \
    gcc \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Run scraper
CMD ["python", "main.py"]
