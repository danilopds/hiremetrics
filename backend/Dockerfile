FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Enable system Python (no virtual environment needed in Docker)
ENV UV_SYSTEM_PYTHON=1

# Copy dependency files first to leverage Docker cache
COPY pyproject.toml ./

# Install dependencies directly to system Python (much faster, no venv overhead)
RUN uv pip install --no-cache .

# Copy the rest of the application
COPY . .

# Use PORT environment variable for Render.com deployment, fallback to 8000 for local development
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"] 