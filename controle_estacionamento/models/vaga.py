class Vaga:
    def __init__(self, numero):
        self.numero = numero
        self.esta_ocupada = False
        self.veiculo_atual = None

    def ocupar(self, veiculo):
        self.esta_ocupada = True
        self.veiculo_atual = veiculo

    def desocupar(self):
        self.esta_ocupada = False
        self.veiculo_atual = None