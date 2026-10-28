FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    DEMO_MODE=true

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose port (Cloud Run defaults to $PORT)
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
