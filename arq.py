import serial
import enq
from enum import Enum

class PROTOS(Enum):
    IPV4 = b'\x00'
    IPV6 = b'\x01'

class estados(Enum):
    OCIOSO = 0
    ACK = 1

class eventos(Enum):
    PAYLOAD = 1   
    ACK = 2
    DADO = 3
    TIMEOUT = 4


class ARQ:
    def __init__(self, ser, tun, session):
        self.controle = b'' # byte de controle
        self.seq_N = False # bit de sequencia TX
        self.seq_M = False # bit de sequencia RX
        self.session = session # id da sessao
        self.payload = b'' # mensagem a ser enviado
        self.data = b'' # pacote recebido
        self.estado = estados.OCIOSO # estado inicial
        self.evento = None # evento nulo
        self.enq = enq.Enquadramento(ser, self) # objeto da classe enquadramento
        self.n_tentativas = 0 # numero de tentativas de trasmissao
        self.proto = b''
        self.tun = tun

    def envia_ok(self):
        return (self.estado == estados.OCIOSO)

    def proto_2Bto1B(proto):
        if(proto == b'8000'):
            return PROTOS.IPV4
        elif(proto == b'866D'):
            return PROTOS.IPV6

    def proto_1Bto2B(proto):
        if(proto == PROTOS.IPV4):
            return b'8000'
        elif(proto == PROTOS.IPV6):
            return b'866D'

    def envia_quadro(self):
        if(self.seq_N):
            self.controle = b'\x08'
        else:
            self.controle = b'\x00'
        self.enq.envia(self.controle +  self.session.to_bytes(1, byteorder='big') + self.proto + self.payload)

    def envia_ack(self):
        self.enq.envia((self.data[1][0] + 0x80).to_bytes(1, byteorder='big') + 
                        self.data[1][1].to_bytes(1, byteorder='big') + 
                        self.data[1][2])

        if(bool(self.data[1][0] & (1 << 3)) == self.seq_M):
            self.seq_M = not(self.seq_M)
            return 1
        else:
            return 0

    def handle_frame(frame):
        self.payload = frame[1]
        self.proto = proto_2Bto1B(frame[0])
        self.evento = eventos.PAYLOAD
        self.handle()


    def handle_data(self, frame):
        self.data = frame 
        
        if((self.data[1][0] & 0x80)):
            self.evento = eventos.ACK
        else:
            print("DADO")
            self.evento = eventos.DADO
        
        status = self.handle()
        if(status[0] == 2):
            self.tun.send_frame((status[1][1:]), proto_1Bto2B(status[1][0]))

    def handle_timeout(self):
        self.evento = eventos.TIMEOUT
        status = self.handle()

    def handle(self):
        if(self.estado == estados.OCIOSO):
            if(self.evento == eventos.PAYLOAD):
                self.envia_quadro()
                print("PAYLOAD")
                self.estado = estados.ACK
                
            elif(self.evento == eventos.DADO):
                #self.data = self.enq.recebe()
                if(not(self.envia_ack())):             
                    self.evento = None
                else:
                    print(self.data[1][2:])
                    return(2, self.data[1][2:])

            elif(self.evento == eventos.TIMEOUT):
                self.n_tentativas += 1
                if(self.n_tentativas == 3):
                    self.n_tentativas = 0
                    return (-3,None)


        else:#ACK
            if(self.evento == eventos.ACK):
                if((self.data[1][0] & 0x08) == (int.from_bytes(self.controle, 'big') & 0x08)):
                    PRINT(ACK)
                    self.estado = estados.OCIOSO
                    self.seq_N = not(self.seq_N)
                    return(1, None)
                else:
                    self.envia_quadro()

            elif(self.evento == eventos.DADO):
                if(not(self.envia_ack())):                
                    self.evento = None
                else:
                    return(2, self.data[1][2:])
            
            elif(self.evento == eventos.TIMEOUT):
                self.n_tentativas += 1
                if(self.n_tentativas == 3):
                    self.n_tentativas = 0
                    return (-3,None)