import textwrap

def menu():
    menu = """\n
    Bem-vindo ao sistema bancário!
    Selecione uma opção:
    
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n Depósito realizado com sucesso!")
    else:
        print("\n Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("\n Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("\n Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("\n Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n Saque realizado com sucesso!")
    else:
        print("\n Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato

def mostrar_extrato(saldo, /, *, extrato):
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")

def cadastrar_cliente(usuarios):
    cpf = input("Digite seu CPF (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário já cadastrado!")
        return
    
    
    nome = input("Digite seu nome: ")
    data_nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
    endereco = input("Digite seu endereço: ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário cadastrado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_contas(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do cliente (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(f"Conta criada para {usuario['nome']} com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuário não encontrado! Cadastre o usuário primeiro.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))

def main():
    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == 'e':
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_contas(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                
        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'nu':
            cadastrar_cliente(usuarios)

        elif opcao == 'q':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Por favor, tente novamente.")
        
main()

