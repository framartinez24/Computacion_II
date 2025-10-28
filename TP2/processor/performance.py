
from __future__ import annotations
import time
import urllib.request
from typing import Dict

def simple_page_fetch(url: str, timeout: float = 20.0) -> tuple[float, int]:
    """Descarga la página principal y retorna (tiempo_ms, tamaño_bytes)."""
    start = time.perf_counter()
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = resp.read()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms, len(data)

def estimate_num_requests(links_in_html: int, images_in_html: int, scripts_in_html: int = 0) -> int:
    base = 1  # la propia página
    return base + images_in_html + scripts_in_html

def analyze_performance(url: str, links_count: int, images_count: int) -> Dict:
    load_ms, size_bytes = simple_page_fetch(url)
    num_req = estimate_num_requests(links_count, images_count)
    return {
        "load_time_ms": int(load_ms),
        "total_size_kb": int(size_bytes / 1024),
        "num_requests": int(num_req),
    }
