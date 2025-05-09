# 1) Base image
FROM python:3.10-slim

# 2) Install Nginx and dependencies
USER root
RUN apt-get update \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

# 3) Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 4) Create non-root user
RUN adduser --disabled-password appuser

# 5) Ensure pip-installed binaries are on PATH
ENV PATH="/home/appuser/.local/bin:$PATH"

# 6) Switch to non-root user
USER appuser

# 7) Set working directory
WORKDIR /app

# 8) Copy application code and nginx config
COPY --chown=appuser:appuser . .

# 9) Switch back to root to configure Nginx
USER root
COPY nginx.conf /etc/nginx/nginx.conf


# 10) Expose ports for Nginx and Uvicorn
EXPOSE 80 8000

# 11) Startup Nginx, then Uvicorn
CMD ["/bin/sh", "-c", "nginx -g 'daemon off;' & uvicorn app.main:app --host 0.0.0.0 --port 8000"]




