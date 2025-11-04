# ============================================================================
# Stage 1: BUILDER - Install dependencies
# ============================================================================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
 && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ============================================================================
# Stage 2: RUNTIME - Minimal production image
# ============================================================================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels

RUN python -m pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir /wheels/* \
 && rm -rf /wheels

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000


# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", "--threads", "4", "--timeout", "60"]