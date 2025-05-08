# Dockerfile

# 1) Base image
FROM python:3.10-slim

# 2) Create non-root user
RUN adduser --disabled-password appuser

# 3) Ensure pip-installed binaries are on PATH
ENV PATH="/home/appuser/.local/bin:$PATH"

# 4) Switch to that user
USER appuser

# 5) Set working dir
WORKDIR /app

# 6) Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7) Copy your app code
COPY . .

# 8) Expose port
EXPOSE 8000

# 9) Run Uvicorn properly (fixed quoting!)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
