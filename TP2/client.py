
#!/usr/bin/env python3
import asyncio
import aiohttp
import json

async def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    args = p.parse_args()

    endpoint = f"http://{args.host}:{args.port}/scrape"
    async with aiohttp.ClientSession() as s:
        async with s.post(endpoint, json={"url": args.url}) as resp:
            data = await resp.json()
            print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
