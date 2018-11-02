import os
import serial
import enq
import arq
import Callback
from tun import Tun
import poller

class protocol:
    def __init__(self, ser, tun, session):
        self.tun = tun
        self.arq = arq.ARQ(ser, self.tun, session)
        self.tun.start()
        self.sched = poller.Poller()
        cbE = Callback.CallbackEnq(self.arq, 0.05)
        cbT = Callback.CallbackTun(self.arq)
        self.sched.adiciona(cbE)
        self.sched.adiciona(cbT)

    def start(self):
        self.sched.despache()