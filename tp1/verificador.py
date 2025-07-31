# verificador.py
import hashlib
import json
import os

class Verificador:
    def __init__(self, queue_frec, queue_pres, queue_oxi, archivo="blockchain.json"):
        self.queue_frec = queue_frec
        self.queue_pres = queue_pres
        self.queue_oxi = queue_oxi
        self.blockchain = []
        self.archivo = archivo
        self.load_blockchain()

    def load_blockchain(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                try:
                    self.blockchain = json.load(f)
                except json.JSONDecodeError:
                    self.blockchain = []

    def calcular_hash(self, prev_hash, datos, timestamp):
        bloque_str = json.dumps(datos, sort_keys=True) + timestamp + prev_hash
        return hashlib.sha256(bloque_str.encode()).hexdigest()

    def construir_bloque(self, datos, timestamp):
        alerta = (
            datos["frecuencia"]["media"] >= 200 or
            datos["oxigeno"]["media"] < 90 or
            datos["oxigeno"]["media"] > 100 or
            datos["presion"]["media"] >= 200
        )

        prev_hash = self.blockchain[-1]["hash"] if self.blockchain else "0" * 64

        bloque = {
            "timestamp": timestamp,
            "datos": datos,
            "alerta": alerta,
            "prev_hash": prev_hash,
            "hash": self.calcular_hash(prev_hash, datos, timestamp)
        }

        self.blockchain.append(bloque)
        self.guardar_bloque()
        print(f"✔️ Bloque #{len(self.blockchain)} guardado | Hash: {bloque['hash']} | Alerta: {alerta}")

    def guardar_bloque(self):
        with open(self.archivo, "w") as f:
            json.dump(self.blockchain, f, indent=4)

    def run(self, cantidad_bloques=60):
        print("📥 Verificador iniciado, esperando resultados...")
        for i in range(cantidad_bloques):
            print(f"🕐 Procesando bloque {i+1}/{cantidad_bloques}")
            frec = self.queue_frec.get()
            pres = self.queue_pres.get()
            oxi = self.queue_oxi.get()

            timestamp = frec["timestamp"]

            datos = {
                "frecuencia": {
                    "media": frec["media"],
                    "desv": frec["desv"]
                },
                "presion": {
                    "media": pres["media"],
                    "desv": pres["desv"]
                },
                "oxigeno": {
                    "media": oxi["media"],
                    "desv": oxi["desv"]
                }
            }

            self.construir_bloque(datos, timestamp)
