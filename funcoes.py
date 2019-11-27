# Todas as funcoes que vão servir para pesquisar na base de dados devem ser implementadas aqui
import psycopg2
import psycopg2.extras
# fgfgfgfgfgfgf
# Coneção à base de dados basica

#hhyyttioooiu

#hhhhhhhh


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

        postgres_insert_query_2 = """ INSERT INTO cliente (utilizador_email) VALUES (%s)"""
        record_to_insert_2 = (user_email,)

        cursor.execute(postgres_insert_query_2, record_to_insert_2)
        connection.commit()
        count = cursor.rowcount
        # DEBUG
        print(count, "Record inserted successfully into clientes table")

    except (Exception, psycopg2.Error):
        if(connection):
            print("Esse email já tem conta criada! Insira outro email.")

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# def check_duplicates(input, coluna, tabela):

    # connection = psycopg2.connect(user="postgres",
            # password="postgres",
            # host="localhost",
            # port="5432",
            # database="Projecto_BD")
    #cursor = connection.cursor()

    #cursor.execute("select %s from %s;", (coluna, tabela))
    # for linha in cursor.fetchall():
        #x = linha[0]
        # print(x)

#hfhfhfhhfhf
