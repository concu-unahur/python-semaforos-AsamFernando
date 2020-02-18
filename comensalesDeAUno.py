import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforoComensal=threading.Semaphore(1)
semaforoCocinero=threading.Semaphore(0)
platosDisponibles = 3

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    while True:
      semaforoCocinero.acquire()
      try:
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      finally:
        semaforoComensal.release()


class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    semaforoComensal.acquire()
    try:
      while platosDisponibles==0:    # se pone el while para q el comensal bloqueado q desperto al cocinero 
        semaforoCocinero.release()   # pregunte si hay platos x q podria desbloquearse cuando es cero y quedan platos negativos
        semaforoComensal.acquire()
      platosDisponibles-=1
      logging.info(f'Que rico! Quedan {platosDisponibles} platos')
    finally:
      semaforoComensal.release()


Cocinero().start()


for i in range(20):
  Comensal(i).start()

