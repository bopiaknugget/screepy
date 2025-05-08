# app/security.py
from pathlib import Path
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

# 1. Read the secret Docker mounted for us
API_KEY_PATH = Path("/run/secrets/api_key")  # default mount point
API_KEY = API_KEY_PATH.read_text().strip() if API_KEY_PATH.exists() else None

# 2. Tell FastAPI which header to look at
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_key(key: str = Security(api_key_header)):
    """Shared dependency that blocks requests without the right key."""
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

