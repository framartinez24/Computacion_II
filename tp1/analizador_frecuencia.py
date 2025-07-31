# analizador_frecuencia.py
import time
import statistics
from collections import deque

def analizador_frecuencia(pipe, queue):
    ventana = deque(maxlen=30)  # Últimos 30 valores

    while True:
        try:
            dato = pipe.recv()
        except EOFError:
            break  # Pipe cerrado

        frecuencia = dato["frecuencia"]
        timestamp = dato["timestamp"]

        ventana.append(frecuencia)

        media = statistics.mean(ventana)
        desv = statistics.stdev(ventana) if len(ventana) > 1 else 0.0

        resultado = {
            "tipo": "frecuencia",
            "timestamp": timestamp,
            "media": media,
            "desv": desv
        }

        queue.put(resultado)
