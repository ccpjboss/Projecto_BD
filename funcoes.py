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

        cursor.execute("SELECT DISTINCT id, n_stock, preco FROM album WHERE album.id = %s;",(op1,))
        id = 0
        quant = 0
        preco = 0
        for linha in cursor.fetchall():
            id = linha[0]
            quant = linha[1]
            preco = linha[2]
        while True:
            op2 = int(input("Insira a quantidade que deseja: "))
            if op2 > quant:
                print("A quantidade que deseja adicionar é superior aos albuns em stock")
            else:
                break
        cursor.execute("INSERT INTO compra (id, data, quantidade, finalizada, valor, cliente_utilizador_email, album_id)"
                        "VALUES(nextval('compra_id_sequence'), now(), %s, False, %s, %s, %s);",(op2,preco,user,op1))
        connection.commit()
        menu.menu_carrinho(user)


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()




def get_musica_id(n):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "SELECT id FROM (SELECT id FROM musica ORDER BY id DESC LIMIT %s) AS x ORDER BY id ASC;", (n,))
        id_musicas = []
        for linha in cursor.fetchall():
            id_musicas.append(linha[0])
        return id_musicas
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def get_id_genero(nome):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM genero WHERE nome = %s;", (nome,))
        for linha in cursor.fetchall():
            return linha[0]

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def get_id_album(nome):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM album WHERE nome = %s;", (nome,))
        for linha in cursor.fetchall():
            return linha[0]

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def get_id_editora(nome):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM editora WHERE nome = %s;", (nome,))
        for linha in cursor.fetchall():
            return linha[0]
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def get_id_artista(nome):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM artista WHERE nome = %s;", (nome,))
        for linha in cursor.fetchall():
            return linha[0]
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def cria_album(a_nome, a_preco, a_nstock, a_data_edicao, a_editora):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("INSERT INTO album VALUES (%s,nextval('album_id_sequence'),%s,true,%s,%s,%s,false);",(a_nome,a_preco,a_nstock,a_data_edicao,a_editora))
        
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into album table")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def cria_musica(musica):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO musica VALUES (nextval('musica_id_sequence'),%s);", (musica,))
        connection.commit()

        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into musica table")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def cria_editora(editora):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO editora VALUES (%s,nextval('editora_id_sequence'));", (editora,))
        connection.commit()

        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into editora table")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def cria_artista(artista):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO artista VALUES (nextval('artista_id_sequence'),%s);", (artista,))
        connection.commit()

        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into artista table")

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def cria_genero(genero):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO genero VALUES (nextval('genero_id_sequence'),%s);", (genero,))
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into genero table")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def insere_artista_album(id_album,id_artista):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO artista_album VALUES (%s,%s);", (id_artista,id_album))
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into artista_album table")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def insere_genero_album(id_album,id_genero):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO genero_album VALUES (%s,%s);", (id_genero,id_album))
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into genero_album table")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def insere_musica_album(id_album,id_musica):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO musica_album VALUES (%s,%s);", (id_musica,id_album))
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into musica_album table")
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()