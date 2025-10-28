
from __future__ import annotations
from typing import Dict
from bs4 import BeautifulSoup

def extract_meta(soup: BeautifulSoup) -> Dict:
    meta = {}

    def first(name: str, prop: str | None = None):
        if prop:
            tag = soup.find("meta", attrs={"property": prop})
            return tag.get("content") if tag and tag.get("content") else None
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content") if tag and tag.get("content") else None

    meta["description"] = first("description")
    meta["keywords"] = first("keywords")

    # Open Graph comunes
    for og in ("og:title", "og:description", "og:type", "og:url", "og:image"):
        meta[og] = first("property", og)

    # Twitter Cards básicas
    for tw in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
        meta[tw] = first("name", tw)

    # Limpieza: eliminar None
    return {k: v for k, v in meta.items() if v}
