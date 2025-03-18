import argparse

# Crear el parser
parser = argparse.ArgumentParser(description="Ejemplo de validación con argparse")

# Definir argumentos
parser.add_argument("-i", "--input", type=str, required=True, help="Archivo de entrada (obligatorio)")
parser.add_argument("-n", "--numero", type=int, help="Un número entero")
parser.add_argument("-v", "--verbose", action="store_true", help="Activar modo detallado")

# Parsear los argumentos
args = parser.parse_args()

# Imprimir los valores
print("Archivo de entrada:", args.input)
if args.numero:
    print("Número:", args.numero)
if args.verbose:
    print("Modo detallado activado.")

