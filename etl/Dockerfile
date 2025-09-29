FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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