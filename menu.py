import funcoes


def menu_inicial():
    print("********************************")
    print("*Welcome to Vynil Records Store*")
    print("********************************")
    print("1.\tLogin")
    print("2.\tNovo ultilizador/Registo")

    while True:
        opcao = int(input("Insira a opção: "))
        if opcao not in [1, 2]:
            print("Insira um opção valida!")
        else:
            break

    if opcao == 1:
        print("Login: ")
        print("Insira o seu e-mail: ")

    elif opcao == 2:
        print("Registo: ")
        while True:
            user_email = input("Insira o email: ")
            if user_email == '':
                print("Não insira um campo vazio!")
            else:
                break
        while True:
            user_password = input("Insira a passwd: ")
            if user_password == '':
                print("Não insira um campo vazio!")
            else:
                break
        while True:
            user_nome = input("Insira o seu nome: ")
            if user_nome == '':
                print("Não insira um campo vazio!")
            else:
                break
    funcoes.novo_user(user_email, user_password, user_nome)


def menu_cliente():
    print("ola")
    print("ola")
