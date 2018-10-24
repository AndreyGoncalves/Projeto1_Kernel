#!/usr/bin/python3
 
import selectors
import sys
 
Timeout = 5 # 5 segundos
 
# um callback para ler do fileobj
def handle(fileobj):
  s = fileobj.readline()
  print('Lido:', s)
 
sched = selectors.DefaultSelector()
sched.register(sys.stdin, selectors.EVENT_READ, handle)
 
while True:
  eventos = sched.select(Timeout)
  if not eventos: # timeout !
    print(eventos)
    print('Timeout !')
  else:
    print(eventos)
    for key,mask in eventos:
      cb = key.data # este é o callback !
      cb(key.fileobj)