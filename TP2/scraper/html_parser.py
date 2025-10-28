
from __future__ import annotations
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urljoin

def parse_basic(html: str, base_url: str) -> Dict:
    soup = BeautifulSoup(html, "lxml")

    title = (soup.title.string.strip() if soup.title and soup.title.string else "")

    # Links normalizados absolutos
    links: List[str] = []
    for a in soup.find_all("a", href=True):
        links.append(urljoin(base_url, a["href"]))

    # Contar headers
    structure = {}
    for level in range(1, 7):
        structure[f"h{level}"] = len(soup.find_all(f"h{level}"))

    # Imágenes
    images: List[str] = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            images.append(urljoin(base_url, src))

    return {
        "title": title,
        "links": links,
        "structure": structure,
        "images": images,
        "images_count": len(images),
        "soup_meta": soup  # para reuso interno (metadata)
    }
