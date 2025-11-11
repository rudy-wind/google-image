from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = FastAPI()

@app.get("/")
def get_images(name: str = Query(..., min_length=1)):
    query = urllib.parse.quote(f"{name} smile face close up")
    url = f"https://www.google.com/search?tbm=isch&q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    image_urls = []
    for img_tag in soup.find_all("img"):
        src = img_tag.get("src")
        if src and src.startswith("http"):
            image_urls.append(src)

    # Ambil maksimal 20 gambar
    image_urls = image_urls[:20]

    return JSONResponse(content={"images": image_urls})
