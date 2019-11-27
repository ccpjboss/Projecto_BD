# Todas as funcoes relacionadas com menus devem ser implementadas aqui
#
#
# this is a change
# stuff on the master branch

import funcoes


def menu_inicial():
    print("********************************")
    print("*Welcome to Vynil Records Store*")
    print("********************************")
    print("1.\tLogin")
    print("2.\tNovo ultilizador/Registo")

    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2'] or opcao == '':
            print("Insira uma opção valida!")
        else:
            break

    if opcao == '1':
        print("Login: ")
        print("Insira o seu e-mail: ")

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
        if opcao not in ['1', '2', '3', '4', '5'] or opcao == '':
            print("Insira uma opção valida!")
        else:
            break
    if opcao == '1':
    elif opcao == '2':
    elif opcao == '3':
    elif opcao == '4':
    elif opcao == '5':
