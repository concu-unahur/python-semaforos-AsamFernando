import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforoComensal=threading.Semaphore(3)
semaforoCocinero=threading.Semaphore(0)
lockComensales=threading.Lock()
comensales=10

class Cocinero(threading.Thread):
  #def __init__(self, numero):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero' #f'Cocinero {numero}'

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

# semaforo para controlar la cantidad de platos correcta ya q el logging tarda mas que los comensales y la cantidad puede ser erronea
# semaforo para q espere el comensal y despierte al cocinero

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
      logging.info(f'Que rico! Quedan {platosDisponibles} platos')
      comensales-=1
    finally:
      if platosDisponibles==0:
        lockComensales.acquire()
        semaforoCocinero.release()
        
platosDisponibles = 3

Cocinero().start()
#Cocinero(1).start()
#Cocinero(2).start()

for i in range(comensales):
  Comensal(i).start()

