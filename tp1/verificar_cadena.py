# verificar_cadena.py
import hashlib
import json
import os

def calcular_hash(prev_hash, datos, timestamp):
    bloque_str = json.dumps(datos, sort_keys=True) + timestamp + prev_hash
    return hashlib.sha256(bloque_str.encode()).hexdigest()

def verificar_integridad(path="blockchain.json"):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print("❌ El archivo blockchain.json está vacío o no existe.")
        return False

    try:
        with open(path, "r") as f:
            blockchain = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False

    if not blockchain:
        print("❌ El archivo está vacío (lista vacía).")
        return False

    errores = []
    for i in range(1, len(blockchain)):
        bloque_anterior = blockchain[i - 1]
        bloque_actual = blockchain[i]

        hash_recalculado = calcular_hash(
            bloque_actual["prev_hash"],
            bloque_actual["datos"],
            bloque_actual["timestamp"]
        )

        if bloque_actual["prev_hash"] != bloque_anterior["hash"]:
            errores.append((i, "prev_hash incorrecto"))

        if bloque_actual["hash"] != hash_recalculado:
            errores.append((i, "hash incorrecto"))

    if errores:
        print("❌ Bloques corruptos detectados:")
        for idx, motivo in errores:
            print(f"  - Bloque #{idx + 1}: {motivo}")
        return False
    else:
        print("✅ Cadena de bloques verificada. No se detectaron errores.")
        return True

def generar_reporte(path="blockchain.json", salida="reporte.txt"):
    with open(path, "r") as f:
        blockchain = json.load(f)

    total = len(blockchain)
    alertas = sum(1 for b in blockchain if b["alerta"])

    suma_frec = suma_pres = suma_oxi = 0
    for b in blockchain:
        suma_frec += b["datos"]["frecuencia"]["media"]
        suma_pres += b["datos"]["presion"]["media"]
        suma_oxi += b["datos"]["oxigeno"]["media"]

    promedio_frec = suma_frec / total
    promedio_pres = suma_pres / total
    promedio_oxi = suma_oxi / total

    with open(salida, "w") as f:
        f.write("REPORTE FINAL\n")
        f.write("=====================\n")
        f.write(f"Bloques totales: {total}\n")
        f.write(f"Bloques con alertas: {alertas}\n")
        f.write(f"\nPromedios generales:\n")
        f.write(f"- Frecuencia: {promedio_frec:.2f}\n")
        f.write(f"- Presión: {promedio_pres:.2f}\n")
        f.write(f"- Oxígeno: {promedio_oxi:.2f}\n")

    print("✅ Reporte generado en reporte.txt")

if __name__ == "__main__":
    if verificar_integridad():
        generar_reporte()
