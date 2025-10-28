
# TP2 — Sistema de Scraping y Análisis Web Distribuido

## Requisitos
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

> Para screenshots reales, instala además Selenium o Playwright (ver más abajo). El proyecto funciona **sin** ellos gracias a un fallback con PIL.

## Ejecución

1. **Servidor de Procesamiento (Parte B)**
```bash
python server_processing.py -i 127.0.0.1 -p 9000 -n 0
```

2. **Servidor de Scraping (Parte A)**
```bash
python server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9000
```

3. **Cliente de prueba**
```bash
python client.py https://example.com --host 127.0.0.1 --port 8000
```

## Endpoints
- `POST /scrape` con JSON `{ "url": "https://sitio" }`
- `GET /scrape?url=https://sitio`

## Formato de Respuesta (ejemplo)
```json
{
  "url": "https://example.com",
  "timestamp": "2025-10-28T12:00:00Z",
  "scraping_data": { "title": "...", "links": ["..."], "meta_tags": {"description": "..."}, "structure": {"h1": 1, "h2": 0}, "images_count": 0 },
  "processing_data": { "screenshot": "base64...", "performance": { "load_time_ms": 200, "total_size_kb": 12, "num_requests": 1 }, "thumbnails": ["base64..."] },
  "status": "success"
}
```

## Captura de pantalla real (opcional)

- **Selenium**
  ```bash
  pip install selenium webdriver-manager
  # Edita `processor/screenshot.py` para usar Selenium si está disponible.
  ```

- **Playwright**
  ```bash
  pip install playwright && playwright install
  # Edita `processor/screenshot.py` para usar Playwright si está disponible.
  ```

## Manejo de errores
- Timeouts en cliente HTTP (30s), validación de URL, manejo de excepciones en ambos servidores.
- Comunicación binaria longitud+JSON; reintentos pueden añadirse en `server_scraping.py`.

## IPv4 / IPv6
- Parte A (aiohttp): bind a `-i` con IPv4 o IPv6.
- Parte B (socketserver): cambia familia automáticamente según IP.

## Bonus (pistas)
- **Task Queue**: agrega endpoints `/status/{id}` y `/result/{id}` almacenando tareas en un `asyncio.Queue` y un `dict` con TTL.
- **Rate limiting & caché**: diccionario `{dominio: token_bucket}` y caché `{url: (resultado, expiry)}`. Para persistencia: Redis.
- **Análisis avanzado**: agrega `processor/seo.py`, `processor/tech_detect.py` y llámalos en `_process_task`.

## Testing
```bash
pytest -q
```

## Notas de implementación
- El Servidor B usa `ThreadingTCPServer` + `ProcessPoolExecutor` para permitir múltiples conexiones concurrentes y paralelizar tareas CPU/IO intensivas.
- El Servidor A nunca bloquea el event loop: el llamado por socket al B se ejecuta en `run_in_executor`.


## Más notas que no sé si alguien leerá
- El código que mejor me funcionó y en 3 terminales es el siguiente: 
- Terminal 1:
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Servidor de Procesamiento (Parte B)
python3 server_processing.py -i 127.0.0.1 -p 9000 

# Servidor Asyncio (Parte A)
python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9000

# Cliente de prueba
python3 client.py https://example.com --host 127.0.0.1 --port 8000


-Terminal 2:
cd ~/Desktop/TP2
source .venv/bin/activate
python3 server_scraping.py -i 0.0.0.0 -p 8000 --proc-ip 127.0.0.1 --proc-port 9000


-Terminal 3:
cd ~/Desktop/TP2
source .venv/bin/activate
python3 client.py https://example.com --host 127.0.0.1 --port 8000

