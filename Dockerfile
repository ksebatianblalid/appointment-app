# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install --no-cache-dir .

# Copy project
COPY src/ ./src/

# Expose port for FastAPI
EXPOSE 8080

# Command to run the app
CMD ["uvicorn", "src.intranet.app:app", "--host", "0.0.0.0", "--port", "8080"]
