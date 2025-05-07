# Use a lightweight Python base image
FROM python:3.10-slim

# Create a user named 'appuser' without a password
RUN adduser --disabled-password appuser

# Set environment variable to include ~/.local/bin in PATH for appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

# Switch to that user for all remaining instructions
USER appuser

# Set working directory inside container
WORKDIR /app

# Copy dependency list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Default command to run the FastAPI app with Uvicorn
CMD ["uvicorn, "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
