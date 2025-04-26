with open('/tmp/fifo_cursor', 'r') as fifo:
    print('Lector 1 lee:', fifo.read(3))
