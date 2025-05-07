import requests

# URL ของ FastAPI ที่รันอยู่
api_url = "http://localhost:8000/scrape"

# รายการ URL ที่ต้องการ scrape
data = {
    "urls": [
        "https://www.bbc.com/news"
    ]
}

# ส่ง HTTP POST ไปที่ API
response = requests.post(api_url, json=data)

# ตรวจสอบผลลัพธ์
if response.status_code == 200:
    for item in response.json():
        print(f"URL: {item['url']}")
        if item['content']:
            print(f"Content (shortened): {item['content']}...\n")
        else:
            print(f"Error: {item['error']}\n")
else:
    print(f"Request failed with status {response.status_code}")
