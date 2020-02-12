import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

# Como un lock, pero yo decido cuántas veces se puede hacer acquire antes de bloquear al thread
# Lo inventó Dijkstra en el ~1962, una de las primeras primitivas de sincronización que existieron
semaphore = threading.Semaphore(5)

semaphore.acquire()
logging.info('quedan 4')
semaphore.acquire()
logging.info('quedan 3')
semaphore.acquire()
logging.info('quedan 2')
semaphore.acquire()
logging.info('queda 1')
semaphore.acquire()
logging.info('quedan 0')

# Acá el programa se bloquea, porque el semáforo ya estaba en 0
semaphore.acquire()
logging.info('esto no se imprime nunca jamás')

# Para salir, apretar Ctrl + C o cerrar la consola
