# Base image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user (best practice)
RUN useradd -m appuser

RUN chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Start app (Django example)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
