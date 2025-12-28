FROM python:3.10-slim

WORKDIR /app

# Dependencias del sistema necesarias para pandas / yfinance
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]