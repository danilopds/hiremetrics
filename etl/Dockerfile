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

# Create directory for DuckDB files
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run dbt commands during build
WORKDIR /app/dbt
RUN dbt clean
RUN dbt deps

# Return to app directory
WORKDIR /app

# Command to run the ETL process
#CMD ["python", "src/ingest_jobs_data.py"]
CMD ["tail", "-f", "/dev/null"]