# analizador_oxigeno.py
import time
import statistics
from collections import deque

def analizador_oxigeno(pipe, queue):
    ventana = deque(maxlen=30)  # Últimos 30 valores

    while True:
        try:
            dato = pipe.recv()
        except EOFError:
            break  # Pipe cerrado

        oxigeno = dato["oxigeno"]
        timestamp = dato["timestamp"]

        ventana.append(oxigeno)

        media = statistics.mean(ventana)
        desv = statistics.stdev(ventana) if len(ventana) > 1 else 0.0

        resultado = {
            "tipo": "oxigeno",
            "timestamp": timestamp,
            "media": media,
            "desv": desv
        }

        queue.put(resultado)
