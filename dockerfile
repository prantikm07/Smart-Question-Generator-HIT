# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (required for some Python libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Set the command to start your application
CMD ["python", "backend/app.py"]