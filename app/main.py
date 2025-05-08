from fastapi import FastAPI, HTTPException, Depends
from typing import List
import requests
from pydantic import BaseModel
from bs4 import BeautifulSoup
from app.security import verify_key  # API key dependency

app = FastAPI()


# Request body schema
class ScrapeRequest(BaseModel):
    urls: List[str]


def clean_html(html_content: str) -> str:
    """
    Use BeautifulSoup to strip scripts, styles, headers, etc.,
    then return the text from <main>, <article>, or <body>.
    """
    soup = BeautifulSoup(html_content, 'lxml')

    for element in soup(['script', 'style', 'footer', 'nav', 'header']):
        element.decompose()

    main_content = soup.find('main') or soup.find('article') or soup.body
    if main_content:
        return main_content.get_text(separator='\n', strip=True)

    return ""


@app.post("/scrape", dependencies=[Depends(verify_key)])
async def scrape_urls(request: ScrapeRequest):
    results = []
    for url in request.urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = clean_html(response.text)
                if content:
                    results.append({
                        "url": url,
                        "content": content
                    })
                else:
                    results.append({
                        "url": url,
                        "error": "No content found after cleaning"
                    })
            else:
                results.append({
                    "url": url,
                    "error": f"HTTP {response.status_code}"
                })
        except Exception as e:
            results.append({
                "url": url,
                "error": f"Error: {str(e)}"
            })

    if not results:
        raise HTTPException(status_code=500, detail="Scraping failed")

    return results
