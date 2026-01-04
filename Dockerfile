# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build deps for compiling Python packages (like psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install deps (using no-cache and without pip cache)
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

# Copy only the built venv (dependencies)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a lightweight non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy only the necessary files (no cache, no git)
COPY app ./app
COPY main.py .

# Expose port
EXPOSE 8000

# Switch to non-root user
USER appuser

CMD ["python3", "main.py"]
