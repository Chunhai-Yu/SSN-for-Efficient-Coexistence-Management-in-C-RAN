import threading
import time
import numpy as np

global a
a=[]
def worker():
    while 1:
        print(threading.currentThread().getName(), 'fetch')
        time.sleep(2)
        print(a[-1], 'what')
        print(threading.currentThread().getName())

def my_service():
    while 1:
        print(threading.currentThread().getName(), 'generate')
        b = np.random.randint(1, 20, 2)
        time.sleep(1)
        a.append(b)
        print(a)

def worker2():
    while 1:
        print(threading.currentThread().getName(), 'none')
        time.sleep(1)
        print(threading.currentThread().getName())


t = threading.Thread(name='my_service', target=my_service)
w = threading.Thread(name='worker', target=worker)
w2=threading.Thread(name='worker2', target=worker2)

t.start()

w.start()
w2.start()