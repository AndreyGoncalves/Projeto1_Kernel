import serial
from enum import Enum

class estados(Enum):
    OCIOSO = 0
    ACK = 1

class eventos(Enum):
    PAYLOAD = 1   
    ACK = 2
    DADO = 3
    TIMEOUT = 4


class ARQ:
    def __init__(self, enq, session):
        self.controle = b'' # byte de controle
        self.seq_N = False # bit de sequencia TX
        self.seq_M = False # bit de sequencia RX
        self.session = session # id da sessao
        self.payload = b'' # mensagem a ser enviado
        self.data = b'' # pacote recebido
        self.estado = estados.OCIOSO # estado inicial
        self.evento = None # evento nulo
        self.enq = enq # objeto da classe enquadramento
        self.n_tentativas = 0 # numero de tentativas de trasmissao
       
    def bytes(data):
        return data.to_bytes(1, byteorder='big')

    def envia(self, payload):
        self.payload = payload
        self.evento = eventos.PAYLOAD
        self.handle()

        while(self.estado != estados.OCIOSO):
            self.enq.set_Timeout(1)
            self.data = self.enq.recebe()
            if(self.data == -3):
                self.evento = eventos.TIMEOUT
                response = self.handle()
                if(response == -3):
                    return -3
            

            elif(self.data[0] > 0):
                #if(self.data[1][1] == self.session):
                self.n_tentativas = 0
                if(self.data[1][0] & 0x80):
                    self.evento = eventos.ACK
                else:
                    self.evento = eventos.DADO
                self.handle()
        self.seq_N = not(self.seq_N)
        return 1


    def recebe(self):
        self.evento = None
        while(self.evento != eventos.DADO):
            self.data = self.enq.recebe()
            if(self.data[0] == -3):
                self.evento = eventos.TIMEOUT
                response =self.handle()
                if(response == -3):
                    return (-3,None)
            elif(self.data[0] > 0):
                #if(self.data[1][1] == self.session):
                self.n_tentativas = 0
                if(self.data[1][0] & 0x80):
                    self.evento = eventos.ACK
                else:
                    self.evento = eventos.DADO
                self.handle()

        return (1, self.data[1][2:])

    def gera_evento(self, eventos):
        self.evento = eventos

    def envia_quadro(self):
        if(self.seq_N):
            self.controle = b'\x08'
        else:
            self.controle = b'\x00'
        self.enq.envia(self.controle + self.session.to_bytes(1, byteorder='big')+ self.payload)

    def envia_ack(self):
        self.enq.envia((self.data[1][0] + 0x80).to_bytes(1, byteorder='big') + 
                        self.data[1][1].to_bytes(1, byteorder='big'))

        if(bool(self.data[1][0] & (1 << 3)) == self.seq_M):
            self.seq_M = not(self.seq_M)
            return 1
        else:
            return 0

    def handle(self):
        if(self.estado == estados.OCIOSO):
            if(self.evento == eventos.PAYLOAD):
                self.envia_quadro()
                self.estado = estados.ACK
                
            elif(self.evento == eventos.DADO):
                self.data = self.enq.recebe()
                if(not(self.envia_ack())):             
                    self.evento = None
                

            elif(self.evento == eventos.TIMEOUT):
                self.n_tentativas += 1
                if(self.n_tentativas == 3):
                    self.n_tentativas = 0
                    return (-3,None)


        else:#ACK
            if(self.evento == eventos.ACK):
                self.data = self.enq.recebe()
                if((self.data[1][0] & 0x08) == (int.from_bytes(self.controle, 'big') & 0x08)):
                    self.estado = estados.OCIOSO
                else:
                    pass
            elif(self.evento == eventos.DADO):
                if(not(self.envia_ack())):                
                    self.evento = None
            
            elif(self.evento == eventos.TIMEOUT):
                self.n_tentativas += 1
                if(self.n_tentativas == 3):
                    self.n_tentativas = 0
                    return (-3,None)