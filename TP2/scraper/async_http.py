
from __future__ import annotations
import aiohttp

DEFAULT_HEADERS = {
    "User-Agent": "TP2-Scraper/1.0 (+https://example.edu)"
}

class HTTPClient:
    def __init__(self, timeout_s: float = 30.0, max_connections: int = 20):
        timeout = aiohttp.ClientTimeout(total=timeout_s)
        conn = aiohttp.TCPConnector(limit=max_connections, force_close=True)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=conn, headers=DEFAULT_HEADERS)

    async def get_text(self, url: str) -> str:
        async with self.session.get(url, allow_redirects=True) as resp:
            resp.raise_for_status()
            return await resp.text()

    async def get_bytes(self, url: str) -> bytes:
        async with self.session.get(url, allow_redirects=True) as resp:
            resp.raise_for_status()
            return await resp.read()

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
