# Todas as funcoes relacionadas com menus devem ser implementadas aqui

import funcoes


def menu_inicial():
    print("********************************")
    print("*Welcome to Vynil Records Store*")
    print("********************************")
    print("1.\tLogin")
    print("2.\tNovo ultilizador")

    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2']:
            print("Insira uma opção valida!")
        else:
            break

    if opcao == '1':
        print("Login: ")
        while True:
            email_input = input("E-mail: ")
            if email_input == '' or ' ' in email_input:
                print("Não insira um campo vazio...")
            else:
                break
        while True:
            passwd_input = input("Password: ")
            if passwd_input == '':
                print("Não insira um campo vazio...")
            else:
                break
        if funcoes.check_login(email_input, passwd_input) == 'cliente':
            print("Login bem sucedido!", email_input)
        elif funcoes.check_login(email_input, passwd_input) == 'admin':
            print("Admin ", email_input, " bem vindo!")
            menu_admin(email_input)
        elif funcoes.check_login(email_input, passwd_input) == 0:
            print("Login invalido!")
            menu_inicial()

    elif opcao == '2':
        print("Registo: ")
        while True:
            user_email = input("Insira o email: ")
            if (user_email == '' or ' ' in user_email):
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
        funcoes.insere_novo_user(user_email, user_password, user_nome)
        menu_inicial()


def menu_cliente():
    print("********************************")
    print("*********Menu Principal*********")
    print("********************************")
    print("1.\tListar todos os albuns")
    print("2.\tCarrinho")
    print("3.\tHistórico de compras")
    print("4.\tMensagens")
    print("5.\tPesquisar")

    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3', '4', '5']:
            print("Insira uma opção valida!")
        else:
            break
    if opcao == '1':
        print()
    elif opcao == '2':
        print()
    elif opcao == '3':
        print()
    elif opcao == '4':
        print()
    elif opcao == '5':
        print()


def menu_admin(user):
    print("Admin: ", user)
    print("1.\tAdicionar álbum.")
    print("2.\tVisualizar álbuns em stock e quantidades.")
    print("3.\tEnviar mensagens.")
    print("4.\tAumentar saldo de um cliente.")
    print("5.\tEstatistica da loja.")
    print("6.\tSair.")
    while True:
        opcao = input("Insira uma opção: ")
        if opcao not in ['1', '2', '3', '4', '5', '6']:
            print("Insira uma opção valida!")
        else:
            break
    if opcao == '1':
        print()
    elif opcao == '2':
        print()
    elif opcao == '3':
        print()
    elif opcao == '4':
        print()
    elif opcao == '5':
        print()
    elif opcao == '6':
        print("Xau")
        exit()
