# Todas as funcoes relacionadas com menus devem ser implementadas aqui

import funcoes
import getpass
from datetime import datetime


def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


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
            passwd_input = getpass.getpass('Password:')
            if passwd_input == '':
                print("Não insira um campo vazio...")
            else:
                break
        if funcoes.check_login(email_input, passwd_input) == 'cliente':
            print("Login bem sucedido!", email_input)
            menu_cliente(email_input)
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
            user_password = getpass.getpass('Password:')
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


def menu_cliente(user):
    print("********************************")
    print("*********Menu Principal*********")
    print("********************************")
    print("Cliente:", user)
    print("1.\tListar todos os albuns")
    print("2.\tCarrinho")
    print("3.\tHistórico de compras")
    print("4.\tMensagens")
    print("5.\tPesquisar")
    print("6.\tSair")

    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3', '4', '5', '6']:
            print("Insira uma opção valida!")
        else:
            break
    if opcao == '1':
        print()
        funcoes.listar_albuns(user)
    elif opcao == '2':
        print()
        menu_carrinho(user)
    elif opcao == '3':
        print()
        funcoes.historico_compra(user)
    elif opcao == '4':
        print()
    elif opcao == '5':
        print()
    elif opcao == '6':
        print("Obrigado e volte sempre!")
        exit()


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
        while True:
            album_nome = input("Nome: ")
            if album_nome == '':
                print("Não insira um campo vazio")
            else:
                break
        while True:
            album_preco = float(input("Preço "))
            if album_preco == 0:
                print("Erro preço não pode ser zero")
            else:
                break
        while True:
            album_nstock = int(input("Qual vai ser o stock inicial: "))
            if album_nstock == 0:
                print("Não pode ser 0")
            else:
                break
        while True:
            print("Insira no formato yyyy-mm-dd")
            album_data_edicao = input("Data de edição: ")
            if validate(album_data_edicao) == False:
                print("Insira a data no formato pedido!")
            else:
                break
        while True:
            album_editora = input("Editora: ")
            if album_editora == '':
                print("Não insira um campo vazio")
            else:
                break
        # Vai buscar o id da editora e guarda
        id_editora = funcoes.get_id_editora(album_editora)

        # Se a funcao retornar none quer dizer que não existe nenhuma editora com aquele nome
        if id_editora == None:
            funcoes.cria_editora(album_editora)  # Cria a editora inserida
        # Vai buscar o id da editora e guarda
        id_editora = funcoes.get_id_editora(album_editora)

        while True:
            album_artista = input("Artista: ")
            if album_artista == '':
                print("Não insira um campo vazio")
            else:
                break
        id_artista = funcoes.get_id_artista(album_artista)

        if id_artista == None:
            funcoes.cria_artista(album_artista)
        id_artista = funcoes.get_id_artista(album_artista)

        while True:
            album_genero = input("Genero: ")
            if album_genero == '':
                print("Não insira um campo vazio")
            else:
                break
        id_genero = funcoes.get_id_genero(album_genero)

        if id_genero == None:
            funcoes.cria_genero(album_genero)
        id_genero = funcoes.get_id_genero(album_genero)

        id_musicas = []  # lista com o id das musicas
        while True:
            n = int(input("Quantas musicas tem o album: "))
            if n == 0:
                print("O album não pode ter 0 musicas!")
            else:
                break

        for i in range(0, n):
            while True:
                nome_musica = input("Musica: ")
                if nome_musica == '':
                    print("Não insira um campo vazio")
                else:
                    funcoes.cria_musica(nome_musica)
                    break

        id_musicas = funcoes.get_musica_id(n)
        funcoes.cria_album(album_nome, album_preco, album_nstock,
                           album_data_edicao, id_editora)
        id_album = funcoes.get_id_album(album_nome)

        funcoes.insere_artista_album(id_album, id_artista)
        funcoes.insere_genero_album(id_album, id_genero)

        for i in id_musicas:
            funcoes.insere_musica_album(id_album, i)

        funcoes.insere_historico_preco(user, id_album, album_preco)
        menu_admin(user)
    elif opcao == '2':
        funcoes.visualiza_albuns_stock(user)
        menu_acoes_admin(user)
    elif opcao == '3':
        print()
    elif opcao == '4':
        funcoes.aumenta_saldo(user)
        menu_admin(user)
    elif opcao == '5':
        menu_estatisticas(user)
    elif opcao == '6':
        print("Xau")
        exit()


def menu_detalhes(user):
    print()
    print("1.\tVer detalhes de um album")
    print("2.\tSair")
    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2']:
            print("Insira uma opção válida!")
        else:
            break
    if opcao == '1':
        funcoes.detalhes_album(user)
    elif opcao == '2':
        menu_cliente(user)


def menu_acoes_admin(user):
    print()
    print("1. \tAções sobre um album")
    print("2. \tSair")
    while True:
        opcao = input("Insira uma opcão: ")
        if opcao not in ['1', '2']:
            print("Insira uma opcão valida")
        else:
            break
    if opcao == '1':
        menu_acoes_admin2(user)
    elif opcao == '2':
        menu_admin(user)


def menu_acoes_admin2(user):
    print("**********Ações**********")
    print("1. \tCorrigir preços")
    print("2. \tVer historico de preços")
    print("3. \tRemover")
    print("4. \tAdicionar stock a um album")
    print("5. \tVoltar ao menu principal")
    while True:
        opcao = input("Insira uma opcão: ")
        if opcao not in ['1', '2', '3', '4', '5']:
            print("Insira uma opcão valida")
        else:
            break
    if opcao == '1':
        funcoes.corrigir_preco(user)
        menu_admin(user)
    elif opcao == '2':
        funcoes.ver_historico_preco(user)
        menu_admin(user)
    elif opcao == '3':
        funcoes.remove_album(user)
        menu_admin(user)
    elif opcao == '4':
        funcoes.update_quanitdade()
        menu_admin(user)
    elif opcao == '5':
        menu_admin(user)


def menu_carrinho(user):
    print("********************************")
    print("************Carrinho************")
    print("********************************")
    print("1.\tVer Albuns no Carrinho")
    print("2.\tAdicionar Album")
    print("3.\tRemover Album")
    print("4.\tFinalizar Compra")
    print("5.\tMenu Principal")
    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3', '4', '5']:
            print("Insira uma opção válida!")
        else:
            break

    if opcao == '1':
        funcoes.ver_carrinho(user)
    elif opcao == '2':
        funcoes.adicionar_carrinho(user)
    elif opcao == '3':
        funcoes.remover_carrinho(user)
    elif opcao == '4':
        funcoes.finalizar_compra(user)
    elif opcao == '5':
        menu_cliente(user)


def menu_estatisticas(user):
    print("************************")
    print("******Estatisticas******")
    print("************************")
    print("1. \tTotal clientes")
    print("2. \tTotal de discos")
    print("3. \tValor total dos discos em stock")
    print("4. \tValor total das vendas")
    print("5. \tTotal de discos por genero")
    print("6. \tTotal de discos por editora")
    print("7. \tAlbuns com falta de stock(<5)")
    print("8. \tSair")

    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3', '4', '5', '6', '7', '8']:
            print("Insira uma opção válida!")
        else:
            break
    if opcao == '1':
        funcoes.total_clientes()
        menu_estatisticas(user)
    elif opcao == '2':
        funcoes.total_albuns()
        menu_estatisticas(user)
    elif opcao == '3':
        funcoes.valor_discos_stock()
        menu_estatisticas(user)
    elif opcao == '4':
        funcoes.valor_vendas()
        menu_estatisticas(user)
    elif opcao == '5':
        funcoes.total_albuns_genero()
        menu_estatisticas(user)
    elif opcao == '6':
        funcoes.total_albuns_editora()
        menu_estatisticas(user)
    elif opcao == '7':
        funcoes.albuns_falta_stock()
        menu_estatisticas(user)
    elif opcao == '8':
        menu_admin(user)
