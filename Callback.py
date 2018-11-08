import poller
import enq
import arq
from tun import Tun

class CallbackEnq(poller.Callback):

    def __init__(self, arq, tout):
        self.arq = arq
        poller.Callback.__init__(self,self.arq.enq.ser, tout)
        

    def handle(self):
        status, frame, proto = self.arq.enq.handle_data()
        if(status == 1):
            #print("Here")
            print(int.from_bytes(proto, byteorder='big'),frame)
            self.arq.tun.send_frame(frame, int.from_bytes(proto, byteorder='big'))

    def handle_timeout(self):
        self.arq.enq.handle_timeout()
        

class CallbackTun(poller.Callback):
    
    def __init__(self, arq):
        self.arq = arq
        poller.Callback.__init__(self, self.arq.tun.fd, 1000)

    def handle(self):
        if(self.arq.envia_ok()):
            proto, msg = self.arq.tun.get_frame()
            
            frame = (proto.to_bytes(2, byteorder='big'), msg)
            #print(frame)
            self.arq.handle_frame(frame)
        
    def handle_timeout(self):
        self.arq.handle_timeout()