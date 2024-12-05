# App Dockerfile
FROM python:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-mysql-client  # MySQL client library for app connection


# Set working directory
WORKDIR /app
COPY ./app /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# Copy requirements and install
COPY app/docker/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

EXPOSE 5050

# Start the app
CMD ["python", "app.py"]
