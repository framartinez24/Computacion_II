
from __future__ import annotations
import socket
import struct
from .serialization import to_json_bytes, from_json_bytes

HEADER = struct.Struct(">I")  # 4 bytes big-endian length

def send_message(sock: socket.socket, obj) -> None:
    payload = to_json_bytes(obj)
    sock.sendall(HEADER.pack(len(payload)))
    sock.sendall(payload)

def recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed while receiving")
        buf += chunk
    return bytes(buf)

def recv_message(sock: socket.socket):
    (length,) = HEADER.unpack(recv_exact(sock, HEADER.size))
    payload = recv_exact(sock, length)
    return from_json_bytes(payload)

def connect(host: str, port: int, timeout: float = 10.0) -> socket.socket:
    # Soporta IPv4/IPv6
    infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    last_err = None
    for family, socktype, proto, canonname, sockaddr in infos:
        try:
            s = socket.socket(family, socktype, proto)
            s.settimeout(timeout)
            s.connect(sockaddr)
            return s
        except OSError as e:
            last_err = e
    raise last_err

def detect_ipv6(ip: str) -> bool:
    return ":" in ip
