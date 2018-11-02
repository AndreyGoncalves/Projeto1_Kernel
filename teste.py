#!/usr/bin/python3

from tun import Tun
import os
import time

tun = Tun("tun1","10.0.0.1","10.0.0.2",mask="255.255.255.252",mtu=1500,qlen=4)

tun.start()

while True:
  print('dormindo por 1 s ...')
  frame = tun.get_frame()
  quadro = frame[0].to_bytes(2, byteorder='big') + frame[1]
  print(quadro)
  time.sleep(1)

