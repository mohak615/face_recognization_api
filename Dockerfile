FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project
COPY . .

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start
CMD ["uvicorn", "face_api:app", "--host", "0.0.0.0", "--port", "8000"]
