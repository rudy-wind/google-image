from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from icrawler.builtin import GoogleImageCrawler
from icrawler.downloader import Downloader
import uuid
import os

app = FastAPI()

# Folder sementara untuk menyimpan gambar
BASE_DIR = "images"
os.makedirs(BASE_DIR, exist_ok=True)

# Custom Downloader untuk nama file acak
class TempDownloader(Downloader):
    def get_filename(self, task, default_ext):
        ext = os.path.splitext(task['file_url'])[1] or default_ext
        return str(uuid.uuid4()) + ext

@app.get("/")
def get_images(name: str = Query(..., min_length=1)):
    keywords = ["smile", "face", "close up"]
    save_dir = os.path.join(BASE_DIR, name.replace(" ", "_"))
    os.makedirs(save_dir, exist_ok=True)
    
    image_urls = []

    for kw in keywords:
        query = f"{name} {kw}"
        crawler = GoogleImageCrawler(
            storage={"root_dir": save_dir},
            downloader_threads=5,
            downloader_cls=TempDownloader
        )
        crawler.crawl(
            keyword=query,
            max_num=10,
            min_size=(1280,720)
        )

    # Ambil semua file yang berhasil di-download
    for f in os.listdir(save_dir):
        # Jika di Vercel, kita bisa kembalikan path relatif
        image_urls.append(f"/{save_dir}/{f}")

    return JSONResponse(content={"images": image_urls})
