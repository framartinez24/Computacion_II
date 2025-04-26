with open('/tmp/fifo_cursor', 'r') as fifo:
    print('Lector 2 lee:', fifo.read(3))
