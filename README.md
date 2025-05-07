# Screepy

A containerized **FastAPI + Scrapy** web‑scraping API with HTML cleaning via BeautifulSoup. Exposes a single /scrape POST endpoint that accepts a list of URLs, crawls each page on demand, strips out scripts/styles/navigation, and returns the fully cleaned text.

---



---

## Features
- **On‑demand scraping**: Each request triggers Scrapy via Crochet integration
- **HTML cleaning**: Removes <script>, <style>, <nav>, <footer>, and other non‑content tags using BeautifulSoup's get_text()
- **Dockerized**: Single Dockerfile builds a reproducible image; runs via Uvicorn on port 8000
- **Simple API**: One POST endpoint /scrape accepting JSON body:
```json
{
  "urls": ["https://example.com", "..."]
}
```

## Prerequisites
* Docker Engine installed on your machine
* (Optional) Git for cloning the repo

## Installation & Running
1. **Clone the repository**
```bash
git clone https://github.com/bopiaknugget/screepy.git
cd screepy
```

2. **Build the Docker image**
```bash
docker build -t bopiaknugget/screepy:latest .
```

3. **Run the container**
```bash
docker run -d --name fastapi-scraper -p 8000:8000 bopiaknugget/screepy:latest
```



## Usage
* **POST** `/scrape`
   * **Request Body**
```json
{
  "urls": [
    "https://www.bbc.com/news",
    "https://example.com"
  ]
}
```
   * **Response**
```json
[
  {
    "url": "https://www.bbc.com/news",
    "content": "Full cleaned text of page…",
    "error": null
  },
  {
    "url": "https://example.com",
    "content": null,
    "error": "HTTP 404"
  }
]
```

## Configuration
No `.env` file required by default. To supply timeouts, proxies, or API keys, extend with Pydantic Settings or pass via `--env-file`.

## .gitignore
```
__pycache__/
*.py[cod]
*.pyo
*.env
*.log
.vscode/
.idea/
```



## License
This project is licensed under the **MIT License**. See the LICENSE file for details.