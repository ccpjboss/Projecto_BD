# Todas as funcoes relacionadas com menus devem ser implementadas aqui

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
            print("Insira um opção valida!")
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
        if funcoes.check_login(email_input, passwd_input):
            print("Login bem sucedido!", email_input)
            # função para ir para o menu cliente
        else:
            print("Email e password não correspondem!")
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
    print("ola")
    print("ola")
