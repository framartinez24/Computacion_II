import sys
import getopt

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:v", ["input=", "output=", "verbose"])
    except getopt.GetoptError as err:
        print("Error:", err)
        sys.exit(2)

    input_file = None
    output_file = None
    verbose = False  # Activaremos esto si se pasa -v

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-v", "--verbose"):
            verbose = True  # Si está presente, lo activamos

    print("Archivo de entrada:", input_file)
    print("Archivo de salida:", output_file)
    if verbose:
        print("Modo detallado activado.")

if __name__ == "__main__":
    main()

