
from __future__ import annotations
import io
from typing import Optional
from PIL import Image, ImageDraw

def _fallback_image(url: str, title: str | None, size=(1200, 800)) -> bytes:
    img = Image.new("RGB", size, (245, 248, 250))
    d = ImageDraw.Draw(img)
    text = f"Screenshot (fallback)\n{url}\n{title or ''}"
    d.multiline_text((40, 40), text, spacing=8)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def make_screenshot(url: str, html: Optional[str] = None, title: Optional[str] = None) -> bytes:
    """Devuelve PNG bytes. Sustituir por Selenium/Playwright si se instalan.
    Por defecto usa un fallback PIL que cumple el mínimo funcional.
    """
    return _fallback_image(url, title)
