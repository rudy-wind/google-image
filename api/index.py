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
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(resp.text, "html.parser")

    image_urls = [img.get("src") for img in soup.find_all("img") if img.get("src")]
    image_urls = image_urls[:20]  # ambil maksimal 20

    return JSONResponse(content={"images": image_urls})
