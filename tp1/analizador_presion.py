# analizador_presion.py
import time
import statistics
from collections import deque

def analizador_presion(pipe, queue):
    ventana = deque(maxlen=30)  # Últimos 30 valores

    while True:
        try:
            dato = pipe.recv()
        except EOFError:
            break  # Pipe cerrado

        presion_sistolica = dato["presion"][0]  # Solo tomamos el primer valor
        timestamp = dato["timestamp"]

        ventana.append(presion_sistolica)

        media = statistics.mean(ventana)
        desv = statistics.stdev(ventana) if len(ventana) > 1 else 0.0

        resultado = {
            "tipo": "presion",
            "timestamp": timestamp,
            "media": media,
            "desv": desv
        }

        queue.put(resultado)
