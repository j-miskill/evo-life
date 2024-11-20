# App Dockerfile
FROM python:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-mysql-client  # MySQL client library for app connection


# Set working directory
COPY ./app /app
WORKDIR /app

# Copy requirements and install
COPY app/docker/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# Start the app
CMD ["python", "app/app.py"]
