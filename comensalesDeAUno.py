import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semaforoComensal=threading.Semaphore(1)
semaforoCocinero=threading.Semaphore(0)
lockComensales=threading.Lock()
platosDisponibles = 3
comensales=25

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
        semaforoComensal.release()

# semaforo para controlar la cantidad de platos correcta ya q el logging tarda mas que los comensales y la cantidad puede ser erronea
# semaforo para q espere el comensal y despierte al cocinero

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    global comensales
    semaforoComensal.acquire() # el 4 comensal tiene q entrar a comer pero si no hay platos tiene q esperar al cocinero
    try:
      if platosDisponibles>0: 
        platosDisponibles -= 1 
        logging.info(f'Que rico! Quedan {platosDisponibles} platos')
      if comensales>0:  
        comensales-=1
    finally:
      if platosDisponibles==0 or comensales==0:
        semaforoCocinero.release()
      else:
        semaforoComensal.release()



        

Cocinero().start()


for i in range(comensales):
  Comensal(i).start()

