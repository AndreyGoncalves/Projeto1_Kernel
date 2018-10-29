import poller
import enq
import arq
from tun import Tun

class CallbackEnq(poller.Callback):

    def __init__(self, enq, tout):
        poller.Callback.__init__(self, enq.ser, tout)
        self.enq = enq

    def handle(self):
        self.enq.handle_data()

    def handle_timeout(self):
        self.enq.handle_timeout()

class CallbackTun(poller.Callback):
    
    def __init__(self, arq):
        poller.Callback.__init__(self, arq.tun.fd, 1000)
        self._tun = arq.tun

    def handle_data(self):
        if(self.arq.envia_ok()):
            arq.handle_frame(self._tun.get_frame())
        
    def handle_timeout(self):
        self.arq.handle_timeout()