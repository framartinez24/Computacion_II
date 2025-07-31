# main.py
import multiprocessing as mp
import time
import random
from datetime import datetime
from analizador_frecuencia import analizador_frecuencia
from analizador_presion import analizador_presion
from analizador_oxigeno import analizador_oxigeno
from verificador import Verificador

def generar_dato():
    return {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)],
        "oxigeno": random.randint(90, 100)
    }

if __name__ == "__main__":
    # Pipes: padre → hijo
    pipe_frec_padre, pipe_frec_hijo = mp.Pipe()
    pipe_pres_padre, pipe_pres_hijo = mp.Pipe()
    pipe_oxi_padre, pipe_oxi_hijo = mp.Pipe()

    # Queues: hijo → verificador
    queue_frec = mp.Queue()
    queue_pres = mp.Queue()
    queue_oxi = mp.Queue()

    # Lanzar procesos analizadores
    proc_frec = mp.Process(target=analizador_frecuencia, args=(pipe_frec_hijo, queue_frec))
    proc_pres = mp.Process(target=analizador_presion, args=(pipe_pres_hijo, queue_pres))
    proc_oxi = mp.Process(target=analizador_oxigeno, args=(pipe_oxi_hijo, queue_oxi))

    proc_frec.start()
    proc_pres.start()
    proc_oxi.start()

    try:
        for _ in range(60):  # 60 segundos de datos
            dato = generar_dato()
            pipe_frec_padre.send(dato)
            pipe_pres_padre.send(dato)
            pipe_oxi_padre.send(dato)
            time.sleep(1)

        # Ejecutar verificador mientras los analizadores aún están activos
        verificador = Verificador(queue_frec, queue_pres, queue_oxi)
        verificador.run(cantidad_bloques=60)

    finally:
        # Cerrar los pipes
        pipe_frec_padre.close()
        pipe_pres_padre.close()
        pipe_oxi_padre.close()

        # Esperar que terminen
        proc_frec.join()
        proc_pres.join()
        proc_oxi.join()
