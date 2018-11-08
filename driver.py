#! /usr/bin/python

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

tun = Tun("tun1",sys.argv[1],sys.argv[2],mask="255.255.255.252",mtu=1500,qlen=4)

#print(sys.argv[1])

ser = serial.Serial(sys.argv[3],9600)
protocol = Protocol.protocol(ser, tun, 0)

protocol.start()
