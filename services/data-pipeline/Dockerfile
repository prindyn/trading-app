FROM python:3.11-bullseye

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        gcc \
        libpq-dev \
        curl \
        ca-certificates \
        build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY services/data-pipeline/requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the code
COPY services/data-pipeline/. /app

# Create tmp directory
RUN mkdir -p /app/tmp/data

# Make entrypoint script executable
RUN chmod +x /app/scripts/entrypoint.sh

# Optional environment flag to enable cron
ENV CRON_ENABLED=true

# Entrypoint
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
