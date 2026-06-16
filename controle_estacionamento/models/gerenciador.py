from models.vaga import Vaga
from models.veiculos import Veiculo
from models.ticket import Ticket

class Estacionamento:

    def __init__(self, total_vagas):
        self.vagas = [
            Vaga(i)
            for i in range(1, total_vagas + 1)]
        self.tickets_ativos = {}

    def registrar_entrada(self, placa, modelo):
        vaga_livre = next(
            (v for v in self.vagas if not v.esta_ocupada),None)
        if not vaga_livre:
            print("\n❌ Estacionamento lotado!")
            return

        novo_veiculo = Veiculo(placa, modelo)
        vaga_livre.ocupar(novo_veiculo)
        novo_ticket = Ticket(novo_veiculo,vaga_livre)
        self.tickets_ativos[placa] = novo_ticket

        print(
            f"\n✅ Veículo {placa} estacionado na Vaga {vaga_livre.numero}!")
        
    def registrar_saida(self, placa):
        if placa not in self.tickets_ativos:
            print("\n❌ Veículo não encontrado.")
            return

        ticket = self.tickets_ativos[placa]
        valor = ticket.fechar_ticket()
        ticket.vaga.desocupar()
        del self.tickets_ativos[placa]
        print(
            f"\n💵 Valor total a pagar: R$ {valor:.2f}")

    def listar_veiculos(self):
        print("\n=== VEÍCULOS ESTACIONADOS ===")
        if len(self.tickets_ativos) == 0:
            print("Nenhum veículo estacionado.")
            return

        for ticket in self.tickets_ativos.values():

            print(f"""Placa: {ticket.veiculo.placa} Modelo: {ticket.veiculo.modelo} Vaga: {ticket.vaga.numero}""")

    def mostrar_vagas(self):
        livres = 0
        for vaga in self.vagas:
            if not vaga.esta_ocupada:
                livres += 1
        print(f"\nVagas disponíveis: {livres}")