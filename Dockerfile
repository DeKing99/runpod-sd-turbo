FROM python:3.10-slim

# Set environment vars to reduce warnings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Set the handler
CMD ["python", "-m", "runpod.serverless.modules.rp_handler"]
