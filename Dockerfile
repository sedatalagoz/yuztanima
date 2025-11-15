FROM python:3.10-slim

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements_web.txt .
RUN pip install --no-cache-dir -r requirements_web.txt

# Uygulama dosyaları
COPY . .

# Uploads klasörü
RUN mkdir -p uploads/agency uploads/users && chmod -R 777 uploads/

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "web_app:app"]
