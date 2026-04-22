# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Copy Python dependencies from builder
COPY --from=builder /usr/local /usr/local

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=pulmonary_api.settings \
    # Cloud Run default port
    PORT=8080

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories as root
RUN mkdir -p /app/media/temp /app/media/upload \
    && chown -R appuser:appuser /app/media

# Switch to non-root user
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Expose 8080 (Cloud Run requirement)
EXPOSE 8080

# Bind to 0.0.0.0:8080
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn pulmonary_api.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 1200"]