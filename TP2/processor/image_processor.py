
from __future__ import annotations
import io
from typing import List
import urllib.request
from PIL import Image

def _download_bytes(url: str, timeout: float = 15.0) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.read()

def make_thumbnails(image_urls: List[str], max_images: int = 3, thumb_size=(240, 240)) -> list[bytes]:
    thumbs: list[bytes] = []
    for url in image_urls[:max_images]:
        try:
            raw = _download_bytes(url)
            im = Image.open(io.BytesIO(raw))
            im.thumbnail(thumb_size)
            buf = io.BytesIO()
            im.save(buf, format="PNG")
            thumbs.append(buf.getvalue())
        except Exception:
            continue
    return thumbs
