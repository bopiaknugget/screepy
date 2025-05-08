#!/usr/bin/env python3
import json
import requests
import sys

api_url = "http://localhost:8000/scrape"


payload = {
    "urls": [
        "https://www.bbc.com/news"
    ]
}


headers = {
    "X-API-Key": "tcIbPqAQySl0a1nCLka6caUSy7D3OnTqhqiK6MXssHk77F4I1P6QuWx3pgTbv7PQ",
    "Content-Type": "application/json"
}

try:
    response = requests.post( api_url, json=payload, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Request failed: {e}")
    sys.exit(1)


try:
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
except ValueError:
    print(response.text)
