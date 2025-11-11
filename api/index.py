from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

API_KEY = "AIzaSyBOmPSJPTYKy-2XXvVgVy59LQi5gDivhc0"  # ganti dengan API Key kamu
CX = "b7c4ed7b825594b0d"        # CX ID Custom Search Engine kamu

@app.get("/")
def get_images(name: str = Query(..., min_length=1)):
    keywords = ["smile", "face", "close up"]
    image_urls = []

    for kw in keywords:
        query = f"{name} {kw}"
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "key": API_KEY,
            "cx": CX,
            "q": query,
            "searchType": "image",
            "num": 10,        # maksimal 10 per query
            "imgSize": "xxlarge"  # ambil HD images
        }

        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()

        for item in data.get("items", []):
            image_urls.append(item.get("link"))

    # Return JSON, maksimal 30 gambar (3 keyword x 10)
    return JSONResponse(content={"images": image_urls})
