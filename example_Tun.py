import os
import time
from tun import Tun

tun = Tun("tun0", "10.0.0.1", "10.0.0.2", mask="255.255.255.252", mtu =1500, qlen=4)
tun.start()

while(True):
    quadro = tun.get_frame()
    print('Recebeu: ',quadro)
    #time.sleep(1) 