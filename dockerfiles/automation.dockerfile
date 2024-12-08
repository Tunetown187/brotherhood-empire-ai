FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set up environment
ENV PYTHONUNBUFFERED=1
ENV SECURE_MODE=true
ENV ANONYMOUS_MODE=true

# Run the application
CMD ["python", "main.py"]
