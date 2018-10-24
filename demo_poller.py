#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:24:35 2018

@author: msobral
"""

import poller
import sys,time

class CallbackStdin(poller.Callback):
    
    def handle(self):
        l = sys.stdin.readline()
        print('Lido:', l)
        return 1
        
    def handle_timeout(self):
        print('Timeout !')
        return -3
   
class CallbackTimer(poller.Callback):

    t0 = time.time()
    
    def __init__(self, tout):
        poller.Callback.__init__(self, None, tout)
        
    def handle_timeout(self):
        print('Timer: t=', time.time()-CallbackTimer.t0)
        return -3
        
cb = CallbackStdin(sys.stdin, 3)
timer = CallbackTimer(2)
sched = poller.Poller()

sched.adiciona(cb)
sched.adiciona(timer)

sched.despache()