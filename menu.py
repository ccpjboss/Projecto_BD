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
    print("3.\tSair")

    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3']:
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
    if opcao == '3':
        exit()


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
        funcoes.mensagem_cliente(user)
    elif opcao == '5':
        pesq = sist_hist()
        menu_pesquisa(user, pesq)
    elif opcao == '6':
        menu_inicial()


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
            try:
                album_preco = float(input("Preço "))
                if album_preco == 0:
                    print("Erro preço não pode ser zero")
                else:
                    break
            except ValueError:
                print("Tem de inserir um numero")
        while True:
            try:
                album_nstock = int(input("Qual vai ser o stock inicial: "))
                if album_nstock == 0:
                    print("Não pode ser 0")
                else:
                    break
            except ValueError:
                print("Tem de inserir um numero")
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

        id_artistas = []  # lista com o id das musicas
        while True:
            try:
                n = int(input("Quantos artistas tem o album: "))
                if n == 0:
                    print("O album não pode ter 0 artistas!")
                else:
                    break
            except ValueError:
                print("Tem de inserir um numero!")

        for i in range(0, n):
            while True:
                nome_artista = input("Artista: ")
                if nome_artista == '':
                    print("Não insira um campo vazio")
                else:
                    if funcoes.get_id_artista(nome_artista) == None:
                        funcoes.cria_artista(nome_artista)
                        id_artistas.append(
                            funcoes.get_id_artista(nome_artista))
                    else:
                        id_artistas.append(
                            funcoes.get_id_artista(nome_artista))
                    break

        id_generos = []  # lista com o id das musicas
        while True:
            try:
                n = int(input("Quantos generos tem o album: "))
                if n == 0:
                    print("O album não pode ter 0 generos!")
                else:
                    break
            except ValueError:
                print("Tem de inserir um numero!")

        for i in range(0, n):
            while True:
                nome_genero = input("Genero: ")
                if nome_genero == '':
                    print("Não insira um campo vazio")
                else:
                    if funcoes.get_id_genero(nome_genero) == None:
                        funcoes.cria_genero(nome_genero)
                        id_generos.append(funcoes.get_id_genero(nome_genero))
                    else:
                        id_generos.append(funcoes.get_id_genero(nome_genero))
                    break

        id_musicas = []  # lista com o id das musicas
        while True:
            try:
                n = int(input("Quantas musicas tem o album: "))
                if n == 0:
                    print("O album não pode ter 0 musicas!")
                else:
                    break
            except ValueError:
                print("Tem de inserir um numero!")

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

        for i in id_generos:
            funcoes.insere_genero_album(id_album, i)

        for i in id_artistas:
            funcoes.insere_artista_album(id_album, i)

        for i in id_musicas:
            funcoes.insere_musica_album(id_album, i)

        funcoes.insere_historico_preco(user, id_album, album_preco)
        menu_admin(user)
    elif opcao == '2':
        funcoes.visualiza_albuns_stock(user)
        menu_acoes_admin(user)
    elif opcao == '3':
        funcoes.envia_mensagem()
        menu_admin(user)
    elif opcao == '4':
        funcoes.aumenta_saldo(user)
        menu_admin(user)
    elif opcao == '5':
        menu_estatisticas(user)
    elif opcao == '6':
        menu_inicial()


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
        funcoes.ver_historico_preco()
        menu_admin(user)
    elif opcao == '3':
        funcoes.remove_album()
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


def menu_pesquisa(user, pesq):
    print("********************************")
    print("************Pesquisa************")
    print("********************************")
    print("Escolha o critério de pesquisa")
    print("1.\tNome Album")
    print("2.\tNome Música")
    print("3.\tGénero")
    print("4.\tArtista")
    print("5.\tMenu Principal")
    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3', '4', '5']:
            print("Insira uma opção válida!")
        else:
            break

    if opcao == '1':
        crit = pesquisa_ordenar(user, pesq)
        ord = asc_desc()
        if pesq == 1:
            funcoes.pesquisa_album(user, crit, ord)
        else:
            funcoes.pesquisa_album_historico(user, crit, ord)
    elif opcao == '2':
        crit = pesquisa_ordenar(user, pesq)
        ord = asc_desc()
        if pesq == 1:
            funcoes.pesquisa_musica(user, crit, ord)
        else:
            funcoes.pesquisa_musica_historico(user, crit, ord)
    elif opcao == '3':
        crit = pesquisa_ordenar(user, pesq)
        ord = asc_desc()
        if pesq == 1:
            funcoes.pesquisa_genero(user, crit, ord)
        else:
            funcoes.pesquisa_genero_historico(user, crit, ord)
    elif opcao == '4':
        crit = pesquisa_ordenar(user, pesq)
        ord = asc_desc()
        if pesq == 1:
            funcoes.pesquisa_artista(user, crit, ord)
        else:
            funcoes.pesquisa_artista_historico(user, crit, ord)

    elif opcao == '5':
        menu_cliente(user)


def pesquisa_ordenar(user, pesq):
    print()
    print("Escolha o critério de ordenação")
    print("1.\tID do album")
    print("2.\tNome do album")
    print("3.\tPreço do album")
    print("4.\tVoltar atrás")
    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2', '3', '4']:
            print("Insira uma opção válida!")
        else:
            break
    if opcao == '1':
        return 'id'
    if opcao == '2':
        return 'nome'
    if opcao == '3':
        return 'preco'
    if opcao == '4':
        menu_pesquisa(user, pesq)


def asc_desc():
    print("Escolha uma ordem")
    print("1.\tAscendente")
    print("2.\tDescendente")
    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2']:
            print("Insira uma opção válida!")
        else:
            break
    if opcao == '1':
        return 'ASC'
    if opcao == '2':
        return 'DESC'


def sist_hist():
    print("Onde pretende pesquisar?")
    print("1.\tSistema")
    print("2.\tHistorico")
    while True:
        opcao = input("Insira a opção: ")
        if opcao not in ['1', '2']:
            print("Insira uma opção válida!")
        else:
            break
    if opcao == '1':
        return 1
    if opcao == '2':
        return 2
