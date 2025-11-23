# Start with Python 3.13 slim image
FROM python:3.13-slim

# Install Chromium and some necessary tools
RUN apt-get update && \
    apt-get install -y chromium wget curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Set environment variable for Chromium location
ENV CHROMIUM_PATH=/usr/bin/chromium

# Set working directory inside container
WORKDIR /app

# Copy all files into container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the main script
CMD ["python", "main.py"]

