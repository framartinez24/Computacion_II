import os

fifo_write = "/tmp/chat2to1"
fifo_read = "/tmp/chat1to2"

# Crear FIFOs si no existen
for fifo in [fifo_write, fifo_read]:
    if not os.path.exists(fifo):
        os.mkfifo(fifo)

# Abrir ambos extremos con O_RDWR para evitar bloqueos
read_fd = os.open(fifo_read, os.O_RDWR)
write_fd = os.open(fifo_write, os.O_RDWR)

# Envolver los descriptores en archivos para usar readline() e input()
with os.fdopen(read_fd, 'r') as fr, os.fdopen(write_fd, 'w') as fw:
    while True:
        try:
            mensaje = fr.readline().strip()
            if mensaje:
                print(f"Otro: {mensaje}")
            msg = input("Vos: ")
            fw.write(msg + '\n')
            fw.flush()
        except KeyboardInterrupt:
            print("\nSaliendo del chat.")
            break
