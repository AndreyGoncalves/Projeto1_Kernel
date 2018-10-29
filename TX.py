import enq
import serial
import arq
import sys
import Callback
import poller
import threading
from tun import Tun
import os
import time
import Protocol

tun = Tun("tun1","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)
ser = serial.Serial('/dev/ttyS0',9600)
protocol = Protocol.protocol(ser, tun, 0)

protocol.start()

# def Scheduller(cb):
  
#   sched = poller.Poller()
#   sched.adiciona(cb)

#   sched.despache()

#ser = serial.Serial('/dev/ttyUSB1',9600)
#data = arq.ARQ(ser, 0)
# cb = Callback.CallbackEnq(data.enq, 5)

# thread = threading.Thread(target=Scheduller(cb), args=(cb,))
# thread.start()
# f=open(sys.argv[1], 'rb')
# while True:
#   l = f.readline()
#   if not l: break
#   data.envia(l)

#   print('enviou:', l)
#data.envia(b'hello\n')
#data.envia(b'How are you\n')
#data.envia(b'Say something\n')
