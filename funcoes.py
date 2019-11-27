import psycopg2


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


def novo_user(user_email, user_passwd, user_nome):
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
        print(count, "Record inserted successfully into utilizadores table")

        # VER AQUI
        postgres_insert_query_2 = """ INSERT INTO cliente (utilizador_email) VALUES (%s)"""
        record_to_insert_2 = (user_email,)

        cursor.execute(postgres_insert_query_2, record_to_insert_2)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into clientes table")

    except (Exception, psycopg2.Error) as error:
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
