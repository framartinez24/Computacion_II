
from __future__ import annotations
import json
import base64
from typing import Any

DEFAULT_JSON_KW = dict(ensure_ascii=False, separators=(",", ":"))

def to_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, **DEFAULT_JSON_KW).encode("utf-8")

def from_json_bytes(data: bytes) -> Any:
    return json.loads(data.decode("utf-8"))

def b64encode_bytes(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")

def b64decode_str(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))
