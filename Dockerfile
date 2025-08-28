# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port 5000
EXPOSE 5000

# Start the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
