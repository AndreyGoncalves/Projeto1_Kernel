#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:24:35 2018

@author: msobral
"""

import poller
import sys,time
from tun import Tun

class CallbackTun(poller.Callback):
    
    def __init__(self, tun):
        poller.Callback.__init__(self, tun.fd, 1000)
        self._tun = tun

    def handle(self):
        l = tun.get_frame()
        print('Lido:', l)
        
    def handle_timeout(self):
        print('Timeout !')
   
class CallbackTimer(poller.Callback):

    t0 = time.time()
    
    def __init__(self, tout):
        poller.Callback.__init__(self, None, tout)
        
    def handle_timeout(self):
        print('Timer: t=', time.time()-CallbackTimer.t0)
        
tun = Tun("tun0","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)
tun.start()

cb = CallbackTun(tun)
timer = CallbackTimer(2)
sched = poller.Poller()

sched.adiciona(cb)
#sched.adiciona(timer)

sched.despache()
