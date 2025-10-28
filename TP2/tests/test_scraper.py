
import asyncio
import aiohttp

async def test_scraper_endpoint():
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/scrape", json={"url": "https://example.com"}) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["status"] == "success"
            assert "scraping_data" in data
