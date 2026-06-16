from models.gerenciador import Estacionamento

if __name__ == "__main__":

    estacionamento = Estacionamento(5)
    while True:

        print("\n=== MENU ESTACIONAMENTO ===")
        print("1 - Registrar Entrada")
        print("2 - Registrar Saída")
        print("3 - Listar Veículos")
        print("4 - Mostrar Vagas")
        print("5 - Sair")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            placa = input("Digite a placa: ")
            modelo = input("Digite o modelo: ")
            estacionamento.registrar_entrada(placa,modelo)

        elif opcao == "2":
            placa = input("Digite a placa: ")
            estacionamento.registrar_saida(placa)

        elif opcao == "3":
            estacionamento.listar_veiculos()

        elif opcao == "4":
            estacionamento.mostrar_vagas()

        elif opcao == "5":
            print("\nSistema encerrado.")
            break
        else:
            print("\n❌ Opção inválida.")