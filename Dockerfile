FROM python:3.11-slim

# Install dependencies for Pillow and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Expose port (if needed)
EXPOSE 5000

# Start app using Gunicorn
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--worker-class", "sync"]
