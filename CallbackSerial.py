import poller
import sys, time
import arq

class CallbackSerial(poller.Callback, ARQ):
    def handle(self):
        if(ARQ.estado == estados.OCIOSO):
            ARQ.gera_evento(eventos.PAYLOAD)
            ARQ.handle()
        return 1    

    def handle_timeout(self):
        ARQ.gera_evento(eventos.TIMEOUT)
        ARQ.handle()
        return -3

class CallbackTimer(poller.Callback):
    t0 = time.time()

    def __init__(self, tout):
        poller.Callback.__init__(self, None, tout)

    def handle_timeout(self):
        return -3

