
#!/usr/bin/env python3
from __future__ import annotations
import argparse
import socket
import socketserver
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict

from common.protocol import recv_message, send_message, detect_ipv6
from common.serialization import b64encode_bytes
from processor.screenshot import make_screenshot
from processor.performance import analyze_performance
from processor.image_processor import make_thumbnails

POOL: ProcessPoolExecutor | None = None

def _process_task(task: Dict[str, Any]) -> Dict[str, Any]:
    url = task["url"]
    html = task.get("html")
    title = task.get("title")
    images = task.get("images", [])
    links_count = task.get("links_count", 0)
    images_count = task.get("images_count", len(images))

    # Ejecutar subtareas (CPU/IO-bound) en este proceso
    screenshot_png = make_screenshot(url, html=html, title=title)
    perf = analyze_performance(url, links_count=links_count, images_count=images_count)
    thumbs = make_thumbnails(images, max_images=3)

    return {
        "screenshot": b64encode_bytes(screenshot_png),
        "performance": perf,
        "thumbnails": [b64encode_bytes(t) for t in thumbs],
        "status": "ok",
    }

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            task = recv_message(self.request)
            assert isinstance(task, dict) and task.get("type") == "process_request"
            # Encolar en el pool de procesos
            future = POOL.submit(_process_task, task["payload"])
            result = future.result()  # cada conexión espera su resultado
            send_message(self.request, {"type": "process_response", "payload": result})
        except Exception as e:
            try:
                send_message(self.request, {"type": "process_response", "error": str(e)})
            except Exception:
                pass

class ThreadingTCPServerV4(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

class ThreadingTCPServerV6(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True

def main():
    parser = argparse.ArgumentParser(prog="server_processing.py", description="Servidor de Procesamiento Distribuido")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    parser.add_argument("-n", "--processes", type=int, default=None, help="Número de procesos en el pool (default: CPU count)")
    args = parser.parse_args()

    global POOL
    POOL = ProcessPoolExecutor(max_workers=args.processes)

    ServerCls = ThreadingTCPServerV6 if detect_ipv6(args.ip) else ThreadingTCPServerV4
    with ServerCls((args.ip, args.port), RequestHandler) as server:
        print(f"[Processing] Escuchando en {args.ip}:{args.port} — procesos={POOL._max_workers}")
        try:
            server.serve_forever(poll_interval=0.5)
        finally:
            POOL.shutdown(wait=True, cancel_futures=True)

if __name__ == "__main__":
    main()
