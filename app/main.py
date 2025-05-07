from fastapi import FastAPI, HTTPException
from typing import List
import requests
from pydantic import BaseModel
from bs4 import BeautifulSoup

app = FastAPI()

# สร้าง schema สำหรับรับข้อมูล
class ScrapeRequest(BaseModel):
    urls: List[str]

def clean_html(html_content: str) -> str:
    """
    ใช้ BeautifulSoup ในการทำความสะอาด HTML โดยการเอาแค่ข้อความหลัก (body, article)
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # ลบแท็กที่ไม่จำเป็นออก เช่น script, style, footer, nav, ...
    for element in soup(['script', 'style', 'footer', 'nav', 'header']):
        element.decompose()

    # ดึงแค่เนื้อหาหลักจาก <body> หรือ <article>
    main_content = soup.find('main') or soup.find('article') or soup.body
    if main_content:
        # เอาเฉพาะข้อความที่แยกเป็นบรรทัด ๆ
        return main_content.get_text(separator='\n', strip=True)
    
    return ""

@app.post("/scrape")
async def scrape_urls(request: ScrapeRequest):
    results = []
    for url in request.urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # ใช้ clean_html ในการทำความสะอาด HTML
                content = clean_html(response.text)
                if content:
                    results.append({
                        "url": url,
                        "content": content  # แค่แสดงเนื้อหาช่วงแรก
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
