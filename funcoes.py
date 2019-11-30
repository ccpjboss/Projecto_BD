# Todas as funcoes que vão servir para pesquisar na base de dados devem ser implementadas aqui
import psycopg2
import psycopg2.extras

# Coneção à base de dados basica
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