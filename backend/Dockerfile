# syntax=docker/dockerfile:1
FROM python:3.11-slim

# ARG for build time (default dev)
ARG ENVIRONMENT=dev
# ENV for runtime in container
ENV ENVIRONMENT=${ENVIRONMENT}

ENV PYTHONDONTWRITEBYTECODE 1      # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1             # Disable Python output buffering

# Set working directory inside the container
WORKDIR /app

# Copy requirements folder
COPY requirements/ ./requirements/

# install dynamic requirements based on ENVIRONMENT
RUN pip install --no-cache-dir -r requirements/${ENVIRONMENT}.txt

# Copy the rest of the application code
# In development, this is usually overridden by volume mounts
COPY . .

# Expose default port for Django development server
EXPOSE 8000

# Default command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
