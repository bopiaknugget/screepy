import requests

api_url = "http://localhost:8000/scrape"


data = {
    "urls": [
        "https://www.bbc.com/news"
    ]
}

headers = {
    "X-API-Key": "tcIbPqAQySl0a1nCLka6caUSy7D3OnTqhqiK6MXssHk77F4I1P6QuWx3pgTbv7PQ",
    "Content-Type": "application/json"
}



response = requests.post(api_url, headers=headers, json=data)


if response.status_code == 200:
    for item in response.json():
        print(f"URL: {item['url']}")
        if item['content']:
            print(f"Content (shortened): {item['content']}...\n")
        else:
            print(f"Error: {item['error']}\n")
else:
    print(f"Request failed with status {response.status_code}")
