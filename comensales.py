import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforoComensal=threading.Semaphore(3)
semaforoCocinero=threading.Semaphore(0)
lockComensales=threading.Lock()
comensales=10

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    while comensales>0:
      semaforoCocinero.acquire()
      try:
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      finally:
        for i in range(min(platosDisponibles, comensales)):
          semaforoComensal.release()
        lockComensales.release()
    

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    global comensales
    semaforoComensal.acquire()
    try:
      platosDisponibles -= 1
      logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
      comensales-=1
    finally:
      if platosDisponibles==0:
        lockComensales.acquire()
        semaforoCocinero.release()
        
platosDisponibles = 3

      
Cocinero().start()

for i in range(comensales):
  Comensal(i).start()

