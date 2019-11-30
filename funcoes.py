# Todas as funcoes que vão servir para pesquisar na base de dados devem ser implementadas aqui
import psycopg2
import psycopg2.extras

# Coneção à base de dados basica
import menu


def connect_db():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:

        print("Error while connecting to PostgreSQL", error)

# Insere novo utilizador na base de dados


def insere_novo_user(user_email, user_passwd, user_nome):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO utilizador (email, password, nome) VALUES (%s,%s,%s)"""
        record_to_insert = (user_email, user_passwd, user_nome)

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into utilizadores table")

    except (Exception, psycopg2.Error):
        if(connection):
            print("Esse email já tem conta criada! Insira outro email.")

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def check_login(input_email, input_password):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT utilizador.email, utilizador.password, cliente.utilizador_email FROM utilizador, cliente WHERE utilizador.email =%s AND utilizador.password = %s AND cliente.utilizador_email = %s;",
                       (input_email, input_password, input_email))

        if cursor.rowcount == 1:
            return 'cliente'  # codigo para cliente_login
        else:
            cursor.execute("SELECT utilizador.email, utilizador.password, admin.utilizador_email FROM utilizador, admin WHERE utilizador.email =%s AND utilizador.password = %s AND admin.utilizador_email = %s;",
                           (input_email, input_password, input_email))
            if cursor.rowcount == 1:
                return 'admin'  # codigo para admin_login
            else:
                return 0

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def listar_albuns(user):
    global id_album, nome_album, artista
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id, nome FROM album;" )

        for linha in cursor.fetchall():
            x1 = linha[0]
            x2 = linha[1]
            print("ID:\t",x1, "\tNome: ",x2)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def detalhes_album(user):
    global id_album, nome_album, artista
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id, nome FROM album;")
        album_id = []
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))
        while True:
            op1 = input("Insira o ID do album: ")
            if op1 not in album_id:
                print("Insira uma opção válida!")
            else:
                break

        cursor.execute("SELECT DISTINCT genero_id,artista_id, editora_id, musica_id "
                        "FROM album, artista_album, genero_album, musica_album, editora "
                        "WHERE genero_album.album_id = %s AND artista_album.album_id = %s"
                        " AND album.id = %s AND musica_album.album_id = %s;", (op1, op1, op1, op1))
        genero_id = 0
        artista_id = 0
        editora_id = 0
        for linha in cursor.fetchall():
            genero_id = linha[0]
            artista_id = linha[1]
            editora_id = linha[2]

        cursor.execute("SELECT DISTINCT album.id, album.nome, preco, em_stock, n_stock, data_edicao, editora.nome, "
                        "genero.nome, artista.nome, musica.nome "
                        "FROM album, editora, genero, artista, musica "
                        "WHERE album.id = %s AND editora.id = %s AND genero.id = %s AND artista.id = %s AND "
                        "musica.id IN (SELECT DISTINCT musica_id FROM musica_album WHERE musica_album.album_id "
                        "= %s);", (op1, editora_id, genero_id, artista_id, op1))

        musica = []
        for linha in cursor.fetchall():
            id_album = linha[0]
            nome_album = linha[1]
            preco = linha[2]
            stock = linha[3]
            n_stock = linha[4]
            data_edicao = linha[5]
            editora = linha[6]
            genero = linha[7]
            artista = linha[8]
            musica.append(linha[9])
        print("ID: ", id_album)
        print("Nome: ", nome_album)
        print("Artista: ", artista)
        for i, musicas in enumerate(musica, start=1):
            print("Musica", i, ":", musicas)
        print("Género:", genero)
        print("Editora:", editora)
        print("Data de Edição:", data_edicao)
        print("Preço:", preco, "€")
        if stock is True:
            print("Exemplares em Stock:", n_stock)
        else:
            print("De momento este album não existe em stock")
        menu.menu_cliente(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def adicionar_carrinho(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM album;")
        album_id = []
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))

        while True:
            op1 = input("Insira o ID do album que pretende adicionar: ")
            if op1 not in album_id:
                print("Insira uma opção válida!")
            else:
                break

        cursor.execute("SELECT n_stock FROM album WHERE id = %s;",(op1,))
        stock = 0
        for linha in cursor.fetchall():
            stock = linha[0]

        if stock == 0:
            print("De momento este album não se encontra em stock")
            menu.menu_carrinho(user)

        cursor.execute("SELECT DISTINCT n_stock, preco FROM album WHERE album.id = %s;",(op1,))
        quant = 0
        preco = 0
        for linha in cursor.fetchall():
            quant = linha[0]
            preco = linha[1]
        while True:
            op2 = int(input("Insira a quantidade que deseja: "))
            if op2 > quant:
                print("A quantidade que deseja adicionar é superior aos albuns em stock")
            else:
                break

        cursor.execute("SELECT album_id FROM compra;")
        album_id = []
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))

        if op1 in album_id:
            cursor.execute("SELECT valor, quantidade FROM compra WHERE album_id = %s;",(op1,))
            quant = 0
            val = 0
            for linha in cursor.fetchall():
                val = linha[0]
                quant = linha[1]
            valor1 = preco*op2
            val = val + valor1
            quant = quant + op2
            cursor.execute("UPDATE compra SET quantidade = %s, data = now(), valor = %s WHERE album_id = %s;",(quant,val, op1))
            connection.commit()
            print("Após esta operação o valor total do seu carrinho é: ", val, "€")
            menu.menu_carrinho(user)
        else:
            valor = op2*preco
            cursor.execute("INSERT INTO compra (id, data, quantidade, finalizada, valor, cliente_utilizador_email, album_id)"
                            "VALUES(nextval('compra_id_sequence'), now(), %s, False, %s, %s, %s);",(op2,valor,user,op1))
            connection.commit()
            print("Após esta operação o valor total do seu carrinho é: ", valor, "€")
            menu.menu_carrinho(user)


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def remover_carrinho(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id, preco FROM album;")
        album_id = []
        preco = 0
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))
            preco = linha[1]
        while True:
            op1 = input("Insira o ID do album que pretende remover: ")
            if op1 not in album_id:
                print("Insira uma opção válida!")
            else:
                break

        cursor.execute("SELECT album_id FROM compra;")
        album_id = []
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))

        if op1 not in album_id:
            print("O album que pretende remover não se encontra no carrinho")
            menu.menu_carrinho(user)

        cursor.execute("SELECT quantidade, valor FROM compra WHERE album_id = %s;", (op1,))
        quant = 0
        val = 0
        for linha in cursor.fetchall():
            quant = linha[0]
            val = linha[1]
        while True:
            op2 = int(input("Insira a quantidade que deseja: "))
            if op2 > quant:
                print("A quantidade que deseja remover é superior à quantidade desse album no carrinho")
            else:
                break
        if op2 == quant:
            cursor.execute("DELETE FROM compra WHERE album_id = %s;",(op1,))
            connection.commit()
            menu.menu_carrinho(user)
        quant = quant-op2
        valor1 = preco*op2
        val = val - valor1
        cursor.execute("UPDATE compra SET quantidade = %s, valor = %s WHERE album_id = %s;",(quant,val,op1))
        connection.commit()
        print("Após esta operação o valor total do seu carrinho é: ", val, "€")
        menu.menu_carrinho(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()


def ver_carrinho(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        print()
        cursor.execute("SELECT album_id, quantidade, valor FROM compra;")
        valor = 0
        for linha in cursor.fetchall():
            album_id = linha[0]
            quant = linha[1]
            val = linha[2]
            cursor.execute("SELECT nome FROM album WHERE id =%s;",(album_id,))
            for linha in cursor.fetchall():
                nome = linha[0]
            print("ID do album: ",album_id)
            print("Nome: ", nome)
            print("Quantidade: ", quant)
            print("Valor: ",val)
            print("----//----")
            valor = valor + val

        if valor == 0:
            print("O seu carrinho está vazio")
        else:
            print("O valor total do seu carrinho é: ", valor,"€")
        menu.menu_carrinho(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def finalizar_compra(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")
        cursor = connection.cursor()

        cursor.execute("SELECT saldo, valor FROM cliente, compra;")

        valor = 0
        for linha in cursor.fetchall():
            saldo = linha[0]
            val = linha[1]
            valor = valor + val

        if saldo < valor:
            print("O seu saldo é insuficiente")
            menu.menu_carrinho(user)

        sal = saldo - valor
        cursor.execute("UPDATE cliente SET saldo =%s;",(sal,))
        connection.commit()
        atualiza_stock()
        cursor.execute("DELETE FROM compra WHERE finalizada is false;")
        connection.commit()
        print("Compra Bem sucedida")
        menu.menu_carrinho(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def atualiza_stock():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")
        cursor = connection.cursor()

        cursor.execute("SELECT n_stock, id FROM album WHERE album.id IN(SELECT album_id FROM compra);")

        stock = 0
        for linha in cursor.fetchall():
            n_stock = linha[0]
            id = linha[1]
            cursor.execute("SELECT quantidade FROM compra WHERE album_id = %s;",(id,))
            for linha in cursor.fetchall():
                quant = linha[0]
                stock = n_stock - quant
                cursor.execute("UPDATE album SET n_stock = %s WHERE id = %s;",(stock,id))
                connection.commit()
                if stock == 0:
                    cursor.execute("UPDATE album SET em_stock = false WHERE id = %s;",(id,))
                    connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()