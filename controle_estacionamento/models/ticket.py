from datetime import datetime
import math

class Ticket:

    def __init__(self):
        self.hora_entrada = datetime.now()

    def calcular_valor(self):
        hora_saida = datetime.now()
        tempo = (
            hora_saida - self.hora_entrada
        ).seconds / 60

        if tempo <= 15:
            return 0
        valor = 10

        if tempo > 60:
            tempo_extra = tempo - 60
            blocos = math.ceil(tempo_extra / 15)
            valor += blocos * 3
        return valor