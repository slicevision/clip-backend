FROM python:3.11-slim

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Railway
EXPOSE 8080

# Start app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
