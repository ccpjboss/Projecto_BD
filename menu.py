def menu_inicial():
    print("********************************")
    print("*Welcome to Vynil Records Store*")
    print("********************************")
    print("1.\tLogin")
    print("2.\tNovo ultilizador/Registo")
    opcao = int(input("Insira a opção"))

    if opcao != 1 and opcao != 2:
        print("Insira uma das opcões!")
        while True:
            opcao = int(input("Insira a opção"))
            if opcao == 1 or opcao == 2:
                break
            print("Insira uma das opcões!")
    if opcao == 1:
        print("Login: ")
        print("Insira o seu e-mail: ")

    elif opcao == 2:
        print("Registo: ")
        user_email = input("Insira o seu email: ")
        if user_email == NULL
