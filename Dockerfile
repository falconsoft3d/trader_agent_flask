FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 3000

# Run the application with Gunicorn, forcing port 3000
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "4", "app:app"]
