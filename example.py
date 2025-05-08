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
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
except ValueError:
    print(response.text)
