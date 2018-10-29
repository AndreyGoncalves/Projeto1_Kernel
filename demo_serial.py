#!/usr/bin/python3

from serial import Serial
import poller
import os
import time
from tun import Tun

class CallbackEnq(poller.Callback):

  def __init__(self, tun, tout):
    poller.Callback.__init__(self, tun, tout)
    self.tun = tun

  def handle(self):
    quadro = self.tun.get_frame()
    print('Recebeu: ',quadro)


  def handle_timeout(self):
    print("Timeout!")

tun = Tun("tun0", "10.0.0.1", "10.0.0.2", mask="255.255.255.252", mtu =1500, qlen=4)
tun.start()

cb = CallbackEnq(tun, 5)

sched = poller.Poller()
sched.adiciona(cb)

sched.despache()
