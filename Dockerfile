# Base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Preload database with CSV data
RUN python loader.py

# Expose port for Flask
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]