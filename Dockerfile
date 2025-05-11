FROM nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu22.04

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3.10 python3-pip git && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    pip install --upgrade pip

WORKDIR /app
COPY . .

# Install Python deps
RUN pip install -r requirements.txt

CMD ["python", "handler.py"]