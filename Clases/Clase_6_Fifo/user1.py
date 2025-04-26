import os

fifo_write = "/tmp/chat1to2"
fifo_read = "/tmp/chat2to1"

for fifo in [fifo_write, fifo_read]:
    if not os.path.exists(fifo):
        os.mkfifo(fifo)

read_fd = os.open(fifo_read, os.O_RDWR)
write_fd = os.open(fifo_write, os.O_RDWR)

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
