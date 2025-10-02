# Production Dockerfile for Django on Dokploy
# Single-stage build for reliability

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
# - build-essential: for compiling Python packages
# - libpq-dev: PostgreSQL client library (headers)
# - curl: for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security (non-root)
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/staticfiles /app/mediafiles /app/backups && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies as appuser
USER appuser
RUN pip install --user --no-warn-script-location -r requirements.txt

# Add user's local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code
COPY --chown=appuser:appuser . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/admin/login/ || exit 1

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
