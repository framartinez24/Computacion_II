
#!/usr/bin/env python3
from __future__ import annotations
import argparse
import asyncio
import traceback
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.parse import urlparse

from aiohttp import web

from scraper.async_http import HTTPClient
from scraper.html_parser import parse_basic
from scraper.metadata_extractor import extract_meta
from common.protocol import connect, send_message, recv_message

async def scrape_and_process(url: str, proc_host: str, proc_port: int, http: HTTPClient) -> Dict[str, Any]:
    # Paso 1: Descargar HTML
    html = await http.get_text(url)

    # Paso 2: Parsear
    basic = parse_basic(html, url)
    meta = extract_meta(basic.pop("soup_meta"))

    scraping_data = {
        **{k: v for k, v in basic.items() if k != "images"},
        "meta_tags": meta,
        "title": basic.get("title", ""),
        "links": basic.get("links", []),
        "structure": basic.get("structure", {}),
        "images_count": basic.get("images_count", 0),
    }

    # Paso 3: pedir procesamiento al Servidor B (sockets)
    loop = asyncio.get_running_loop()

    def blocking_socket_call() -> Dict[str, Any]:
        with connect(proc_host, proc_port, timeout=10.0) as s:
            send_message(s, {
                "type": "process_request",
                "payload": {
                    "url": url,
                    "html": html,
                    "title": scraping_data["title"],
                    "images": basic.get("images", [])[:5],
                    "links_count": len(scraping_data["links"]),
                    "images_count": scraping_data["images_count"],
                }
            })
            resp = recv_message(s)
            return resp

    resp = await loop.run_in_executor(None, blocking_socket_call)
    if resp.get("type") != "process_response":
        raise RuntimeError("Respuesta inválida del servidor de procesamiento")
    payload = resp.get("payload")
    if not payload and resp.get("error"):
        raise RuntimeError(resp["error"])

    result = {
        "scraping_data": scraping_data,
        "processing_data": payload,
    }
    return result

async def handle_scrape(request: web.Request) -> web.Response:
    try:
        url = request.query.get("url")
        if request.method == "POST" and not url:
            data = await request.json()
            url = data.get("url")
        if not url:
            raise web.HTTPBadRequest(reason="Falta parámetro 'url'")

        # Validación básica
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            raise web.HTTPBadRequest(reason="URL debe ser http(s)")

        app = request.app
        http: HTTPClient = app["http"]
        proc_host = app["proc_host"]
        proc_port = app["proc_port"]

        combined = await scrape_and_process(url, proc_host, proc_port, http)
        response = {
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **combined,
            "status": "success",
        }
        return web.json_response(response)
    except asyncio.TimeoutError:
        return web.json_response({"status": "error", "error": "timeout"}, status=504)
    except web.HTTPError as e:
        raise
    except Exception as e:
        traceback.print_exc()
        return web.json_response({"status": "error", "error": str(e)}, status=500)

async def make_app(proc_host: str, proc_port: int) -> web.Application:
    app = web.Application()
    app.add_routes([
        web.get("/scrape", handle_scrape),
        web.post("/scrape", handle_scrape),
    ])
    app["http"] = HTTPClient(timeout_s=30.0, max_connections=20)
    app["proc_host"] = proc_host
    app["proc_port"] = proc_port

    async def on_cleanup(app):
        await app["http"].close()

    app.on_cleanup.append(on_cleanup)
    return app

def main():
    parser = argparse.ArgumentParser(prog="server_scraping.py", description="Servidor de Scraping Web Asíncrono")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha (IPv4/IPv6)")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Número de workers (reservado)")
    parser.add_argument("--proc-ip", required=True, help="IP del servidor de procesamiento")
    parser.add_argument("--proc-port", type=int, required=True, help="Puerto del servidor de procesamiento")
    args = parser.parse_args()

    web.run_app(make_app(args.__dict__["proc_ip"], args.__dict__["proc_port"]), host=args.ip, port=args.port)

if __name__ == "__main__":
    main()
