from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from icrawler.builtin import GoogleImageCrawler
from icrawler.downloader import Downloader

app = FastAPI()

# Custom downloader: hanya ambil URL, jangan download file
class URLOnlyDownloader(Downloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = []  # simpan URL di sini

    def download(self, task, default_ext, **kwargs):
        self.urls.append(task['file_url'])
        # Return None supaya tidak download
        return None

@app.get("/")
def get_images(name: str = Query(..., min_length=1)):
    keywords = ["smile", "face", "close up"]
    image_urls = []

    # Gunakan folder sementara, tapi gambar tidak akan disimpan
    save_dir = "tmp"
    
    for kw in keywords:
        query = f"{name} {kw}"
        downloader = URLOnlyDownloader(storage={"root_dir": save_dir})
        crawler = GoogleImageCrawler(downloader_cls=lambda *a, **kw: downloader)
        crawler.crawl(keyword=query, max_num=10, min_size=(1280, 720))
        image_urls.extend(downloader.urls)
        downloader.urls = []  # reset supaya tidak ada duplikat di keyword berikutnya

    return JSONResponse(content={"images": image_urls})
