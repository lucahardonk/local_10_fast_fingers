FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app.py .
COPY templates/ templates/

# Create instance directory for SQLite database
RUN mkdir -p instance

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
