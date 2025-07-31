### BIENVENIDO ###
# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

## 🧠 Descripción General

Este proyecto simula un sistema biométrico distribuido compuesto por múltiples procesos concurrentes que:

- Generan datos biométricos simulados en tiempo real.
- Analizan cada señal de forma paralela mediante mecanismos de comunicación entre procesos (IPC).
- Verifican los resultados y almacenan los análisis en una cadena de bloques local (`blockchain.json`) para garantizar integridad.
- Permiten verificar la integridad de los bloques y generar un reporte resumen (`reporte.txt`).


## 🧩 Estructura del Proyecto

proyecto\_biometrico/
├── main.py                    # Proceso principal (generador)
├── analizador\_frecuencia.py  # Analizador de frecuencia cardíaca
├── analizador\_presion.py     # Analizador de presión sistólica
├── analizador\_oxigeno.py     # Analizador de oxígeno en sangre
├── verificador.py            # Verificador: construcción y guardado de bloques
├── verificar\_cadena.py       # Script externo: verifica cadena + genera reporte
├── blockchain.json           # Archivo generado con los bloques
├── reporte.txt               # Reporte generado al final del proceso
└── README.md                 # Este archivo

## 🚀 Requisitos

- Python **3.9 o superior**
- No se utilizan librerías externas. Solo se requieren:
  - `multiprocessing`
  - `datetime`
  - `random`
  - `queue`
  - `os`
  - `json`
  - `hashlib`
  - `statistics`
  - `collections`

---

## ▶️ Instrucciones de Ejecución

### 1. Ejecutar el sistema completo

Desde una terminal, dentro del directorio del proyecto:

bash
python3 main.py


Esto realiza:

* Generación de 60 muestras (una por segundo).
* Análisis concurrente en tres procesos distintos.
* Cálculo de estadísticas en ventanas móviles.
* Verificación de los resultados.
* Construcción de bloques con hash encadenado.
* Escritura de `blockchain.json` en disco.

Durante la ejecución se mostrarán por consola los bloques creados y su estado de alerta.


### 2. Verificar integridad de la cadena y generar el reporte

Una vez finalizada la ejecución de `main.py`, ejecutar:

```bash
python3 verificar_cadena.py
```

Este script:

* Revisa que todos los bloques estén correctamente encadenados (hash y prev\_hash).
* Informa si existen bloques corruptos.
* Genera el archivo `reporte.txt` con:

  * Cantidad total de bloques.
  * Número de bloques con alertas.
  * Promedio de frecuencia, presión y oxígeno.


## 📄 Archivos Generados

| Archivo           | Descripción                                                       |
| ----------------- | ----------------------------------------------------------------- |
| `blockchain.json` | Cadena de bloques generada con resultados biométricos verificados |
| `reporte.txt`     | Reporte final con resumen estadístico                             |



## ⚙️ Detalles Técnicos

* Cada bloque contiene:

  * Timestamp
  * Resultados promedio y desvío estándar por tipo de señal
  * Hash SHA-256 del bloque anterior (`prev_hash`)
  * Hash del bloque actual (`hash`)
  * Flag de alerta (`true` si los valores están fuera de rango)

* Los procesos usan:

  * `Pipe` para comunicación desde el generador hacia cada analizador.
  * `Queue` para comunicación desde los analizadores hacia el verificador.

* El sistema se ejecuta durante exactamente 60 segundos, procesando una muestra por segundo.

* La lógica de cálculo estadístico usa ventanas móviles de los últimos 30 valores por tipo de dato.


## 📌 Validaciones y Alertas

El verificador marca un bloque con `"alerta": true` si:

* `frecuencia.media >= 200`
* `presion.media >= 200`
* `oxigeno.media < 90` o `> 100`

## 📘 Observaciones

* Si el archivo `blockchain.json` no se genera o aparece vacío, revisar que el verificador esté recibiendo correctamente los datos desde las colas (`Queue`) y que los analizadores estén activos.
* Se recomienda usar `print()` de depuración para verificar el flujo de datos si se detectan errores durante el desarrollo.


## 📚 Créditos

Trabajo práctico 1 de **Computación II**
**Carrera:** Ingeniería en Informática
**Universidad de Mendoza**
**Año:** 2025
**Autor:** Franco Martínez