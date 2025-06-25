# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1      # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1             # Disable Python output buffering

# Set working directory inside the container
WORKDIR /app

# Copy only requirements file to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# In development, this is usually overridden by volume mounts
COPY . .

# Expose default port for Django development server
EXPOSE 8000

# Default command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
