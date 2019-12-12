# Todas as funcoes que vão servir para pesquisar na base de dados devem ser implementadas aqui
import psycopg2
import psycopg2.extras

# Coneção à base de dados basica
import menu

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

    except (Exception, psycopg2.Error):
        if(connection):
            print("Esse email já tem conta criada! Insira outro email.")

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

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
    #global id_album, nome_album, artista
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

        cursor.execute("SELECT DISTINCT editora_id "
                        "FROM album "
                        "WHERE album.id = %s;", (op1,))

        editora_id = 0
        for linha in cursor.fetchall():
            editora_id = linha[0]

        cursor.execute("SELECT DISTINCT album.id, album.nome, preco, em_stock, n_stock, data_edicao, editora.nome "
                        "FROM album, editora "
                        "WHERE album.id = %s AND editora.id = %s;", (op1, editora_id))

        musica = []
        genero = []
        artista = []
        for linha in cursor.fetchall():
            id_album = linha[0]
            nome_album = linha[1]
            preco = linha[2]
            stock = linha[3]
            n_stock = linha[4]
            data_edicao = linha[5]
            editora = linha[6]
            cursor.execute("SELECT DISTINCT nome FROM genero WHERE id IN (SELECT DISTINCT genero_id FROM genero_album WHERE album_id = %s);",(op1,))
            for linha in cursor.fetchall():
                genero.append(linha[0])
            cursor.execute("SELECT DISTINCT nome FROM artista WHERE id IN (SELECT DISTINCT artista_id FROM artista_album WHERE album_id = %s);",(op1,))
            for linha in cursor.fetchall():
                artista.append(linha[0])
            cursor.execute("SELECT DISTINCT nome FROM musica WHERE id IN (SELECT DISTINCT musica_id FROM musica_album WHERE album_id = %s);",(op1,))
            for linha in cursor.fetchall():
                musica.append(linha[0])
        print("ID: ", id_album)
        print("Nome: ", nome_album)
        for i, artistas in enumerate(artista, start=1):
            print("Artista", i, ":", artistas)
        for i, musicas in enumerate(musica, start=1):
            print("Musica", i, ":", musicas)
        for i, generos in enumerate(genero, start=1):
            print("Género", i, ":", generos)
        print("Editora:", editora)
        print("Data de Edição:", data_edicao)
        print("Preço:", preco, "€")
        if stock is True:
            print("Exemplares em Stock:", n_stock)
        else:
            print("De momento este album não existe em stock")
        
        while True:
            move_on = input("Enter para continuar")
            if move_on == '':
                break
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
                print("O ID que pretende adicionar não existe!")
            else:
                break

        cursor.execute("SELECT n_stock FROM album WHERE id = %s;",(op1,))
        stock = 0
        for linha in cursor.fetchall():
            stock = linha[0]

        if stock == 0:
            print("De momento este album não se encontra em stock")
            menu.menu_carrinho(user)

        cursor.execute("SELECT n_stock, preco FROM album WHERE album.id = %s;",(op1,))
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

        cursor.execute("SELECT album_id FROM compra WHERE cliente_utilizador_email = %s AND finalizada = false;",(user,))
        album_id = []
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))

        if op1 in album_id:
            cursor.execute("SELECT valor, quantidade, finalizada FROM compra WHERE album_id = %s AND cliente_utilizador_email = %s;",(op1,user))
            quant = 0
            val = 0
            for linha in cursor.fetchall():
                val = linha[0]
                quant = linha[1]
            valor1 = preco*op2
            val = val + valor1
            quant = quant + op2

            cursor.execute("UPDATE compra SET quantidade = %s, data = now(), valor = %s WHERE album_id = %s AND finalizada = false AND cliente_utilizador_email= %s;",(quant,val, op1,user))
            connection.commit()
        else:
            valor = op2*preco
            cursor.execute("INSERT INTO compra (id, data, quantidade, finalizada, valor, cliente_utilizador_email, album_id)"
                            "VALUES(nextval('compra_id_sequence'), now(), %s, False, %s, %s, %s);",(op2,valor,user,op1))
            connection.commit()

        print("Após esta operação o valor total do seu carrinho é: ", valor_total(user), "€")
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
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))
        while True:
            op1 = input("Insira o ID do album que pretende remover: ")
            if op1 not in album_id:
                print("Insira uma opção válida!")
            else:
                break

        cursor.execute("SELECT album_id FROM compra WHERE finalizada = false AND cliente_utilizador_email = %s;",(user,))
        album_id = []
        for linha in cursor.fetchall():
            album_id.append(str(linha[0]))

        if op1 not in album_id:
            print("O album que pretende remover não se encontra no carrinho")
            menu.menu_carrinho(user)

        cursor.execute("SELECT preco FROM album WHERE id = %s;",(op1,))
        for linha in cursor.fetchall():
            preco = linha[0]
            
        cursor.execute("SELECT quantidade, valor FROM compra WHERE album_id = %s AND finalizada = false AND cliente_utilizador_email = %s;", (op1,user))
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
            cursor.execute("DELETE FROM compra WHERE album_id = %s AND finalizada = false AND cliente_utilizador_email = %s;",(op1,user))
            connection.commit()
            menu.menu_carrinho(user)
        quant = quant-op2
        valor1 = preco*op2
        val = val - valor1
        cursor.execute("UPDATE compra SET quantidade = %s, valor = %s WHERE album_id = %s AND finalizada = false AND cliente_utilizador_email = %s;",(quant,val,op1,user))
        connection.commit()
        print("Após esta operação o valor total do seu carrinho é: ", valor_total(user), "€")
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
        cursor.execute("SELECT album_id, quantidade, valor FROM compra WHERE finalizada = false AND cliente_utilizador_email=%s;",(user,))

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
        if valor_total(user) == 0:
            print("O seu carrinho está vazio")
        else:
            print("O valor total do seu carrinho é: ", valor_total(user),"€")
        menu.menu_carrinho(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def valor_total(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")
        cursor = connection.cursor()

        cursor.execute("SELECT valor FROM compra WHERE finalizada = false AND cliente_utilizador_email = %s;",(user,))

        valor = 0
        for linha in cursor.fetchall():
            val = linha[0]
            valor = valor + val
        return (valor)
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

        cursor.execute("SELECT saldo, valor FROM cliente, compra WHERE utilizador_email = %s AND cliente_utilizador_email = %s AND finalizada = false;",(user,user))

        valor = 0
        for linha in cursor.fetchall():
            saldo = linha[0]
            val = linha[1]
            valor = valor + val

        if saldo < valor:
            print("O seu saldo é insuficiente")
            menu.menu_carrinho(user)

        sal = saldo - valor
        cursor.execute("UPDATE cliente SET saldo =%s WHERE utilizador_email = %s;",(sal,user))
        connection.commit()
        cursor.execute("UPDATE compra SET data2 = now() WHERE finalizada = false AND cliente_utilizador_email = %s;",(user,))
        connection.commit()
        cursor.execute("UPDATE compra SET finalizada = true WHERE cliente_utilizador_email = %s;",(user,))
        atualiza_stock()
        connection.commit()
        cursor.execute("SELECT album_id FROM compra WHERE finalizada = true;")
        for linha in cursor.fetchall():
            id_album = linha[0]
            cursor.execute("UPDATE album SET comprado = true WHERE id = %s;",(id_album,))
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
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def update_quanitdade():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        id_album = []
        cursor.execute("SELECT id FROM album WHERE em_stock = true")
        for linha in cursor.fetchall():
            id_album.append(linha[0])
        print(id_album)
        while True:
            id = int(input("Insira o id do álbum: "))
            if id not in id_album:
                print("Não é possivel selecionar esse álbum")
            else:
                break
        cursor.execute("SELECT n_stock FROM album WHERE id = %s;",(id,))
        for linha in cursor.fetchall():
            stock_atual = linha[0]
            print("O stock atual é: ",stock_atual)

        aumento = int(input("Quanto quer adicionar: "))

        cursor.execute("UPDATE album SET n_stock = %s + %s WHERE id =%s;",(stock_atual,aumento,id))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def visualiza_albuns_stock(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id, nome, n_stock FROM album WHERE em_stock = TRUE;")
        for linha in cursor.fetchall():
            id = linha[0]
            nome = linha[1]
            n_stock = linha[2]
            print("ID:\t",id, "\tNome: ",nome,"\tQuantidade: \t",n_stock)
        
        while True:
            move_on = input("Enter para continuar")
            if move_on == '':
                break
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def insere_historico_preco(user,album_id,preco):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("INSERT INTO historico_preco VALUES (%s,now(),%s,%s,nextval('altera_id_sequence'));",(preco,user,album_id))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def corrigir_preco(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        id_album = []
        cursor.execute("SELECT id FROM album WHERE em_stock = true")
        for linha in cursor.fetchall():
            id_album.append(linha[0])
        print(id_album)
        while True:
            id = int(input("Insira o id do álbum: "))
            if id not in id_album:
                print("Não é possivel selecionar esse álbum")
            else:
                break
        cursor.execute("SELECT preco FROM album WHERE id = %s;",(id,))
        for linha in cursor.fetchall():
            print("O preço atual é: ",linha[0])
        while True:
            novo_preco = float(input("Qual será o novo preco: "))
            if novo_preco == 0:
                print("Valor invalido!")
            else:
                break
        cursor.execute("UPDATE album SET preco = %s WHERE id =%s;",(novo_preco,id))
        connection.commit()

        insere_historico_preco(user,id,novo_preco)

        cursor.execute("UPDATE compra SET valor=quantidade*%s WHERE album_id = %s;",(novo_preco,id))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def ver_historico_preco():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        id_album = []
        cursor.execute("SELECT id FROM album WHERE em_stock = true")
        for linha in cursor.fetchall():
            id_album.append(linha[0])
        print(id_album)
        while True:
            id = int(input("Insira o id do álbum: "))
            if id not in id_album:
                print("Não é possivel selecionar esse álbum")
            else:
                break
        cursor.execute("SELECT preco,data FROM  historico_preco WHERE album_id = %s;",(id,))
        for linha in cursor.fetchall():
            preco = linha[0]
            data = linha[1]
    
            print("Preco: ",preco,"Data: \t",data)
        
        while True:
            move_on = input("Enter para continuar")
            if move_on == '':
                break
            
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def remove_album():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        id_album = []
        id_album_compra = []
        cursor.execute("SELECT id FROM album WHERE comprado = false") #verifica quais albuns ainda não foram comprados
        for linha in cursor.fetchall():
            id_album.append(linha[0])
        
        cursor.execute("SELECT DISTINCT album_id FROM compra") #verifica quais albuns estão nos carrinhos das pessoas
        for linha in cursor.fetchall():
            id_album_compra.append(linha[0])
        
        if id_album == id_album_compra or id_album == []: #se estiverem num carrinho ou já foram comprados então não podem ser removidos
            print("Não existem albuns que possam ser removidos!")
            return
        while True:
            id = int(input("Insira o id do álbum: "))
            if (id not in id_album) or (id in id_album_compra):
                print("Não é possivel selecionar esse álbum! Não existe, já foi comprado ou está no carrinho de uma pessoa")
            else:
                break
        cursor.execute("DELETE FROM artista_album WHERE album_id = %s;",(id,))
        connection.commit()

        cursor.execute("DELETE FROM genero_album WHERE album_id = %s;",(id,))
        connection.commit()

        cursor.execute("DELETE FROM musica_album WHERE album_id = %s;",(id,))
        connection.commit()

        cursor.execute("DELETE FROM historico_preco WHERE album_id = %s;",(id,))
        connection.commit()

        cursor.execute("DELETE FROM album WHERE id = %s",(id,))
        connection.commit()
        
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def aumenta_saldo(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cliente")
        for linha in cursor.fetchall():
            email = linha[1]
            saldo = linha[0]
            print("Email:\t",email, "\tSaldo: ",saldo)
        
        email_cliente = []
        cursor.execute("SELECT utilizador_email FROM cliente")
        for linha in cursor.fetchall():
            email_cliente.append(linha[0])
        
        while True:
            email_input = input("Insira o email do utilizador: ")
            if email_input not in email_cliente:
                print("Esse utilizador não existe...")
            else:
                break
        
        aumento = float(input("Quanto deseja aumentar: "))
        cursor.execute("SELECT saldo FROM cliente WHERE utilizador_email = %s;",(email_input,))
        for linha in cursor.fetchall():
            saldo_antigo = linha[0]
        novo_saldo = saldo_antigo + aumento

        cursor.execute("UPDATE cliente SET saldo = %s WHERE utilizador_email = %s;",(novo_saldo,email_input))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def historico_compra(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT id, data, valor, quantidade, data2, album_id FROM compra WHERE finalizada = true AND cliente_utilizador_email = %s;",(user,))
        for linha in cursor.fetchall():
            id = linha[0]
            data = linha[1]
            valor = linha[2]
            quant = linha[3]
            data2 = linha[4]
            album_id = linha[5]
            cursor.execute("SELECT nome FROM album WHERE id = %s;",(album_id,))
            for linha in cursor.fetchall():
                album_nome = linha[0]
            print("ID da compra: ",id)
            print("ID do album: ", album_id)
            print("Nome do album: ", album_nome)
            print("Quantidade: ", quant)
            print("Valor: ", valor)
            print("Data em que foi adicionado ao carrinho: ", data)
            print("Data em que foi comprado: ", data2)
            print("-------------------//-------------------------")
        total_preco_genero(user)
        
        while True:
            move_on = input("Enter para continuar")
            if move_on == '':
                break
        menu.menu_cliente(user)


    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def total_clientes():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cliente")
        count = cursor.rowcount
        print("Nº de cliente registados: ", count)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def total_albuns():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM album")
        count = cursor.rowcount
        print("Nº de albuns registados no sistema: ", count)
        
        total_stock = 0
        cursor.execute("SELECT n_stock FROM album")
        for linha in cursor.fetchall():
            total_stock += linha[0]
        
        print("Nº de exemplares no sistema: ", total_stock)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def valor_discos_stock():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT sum(n_stock*preco) FROM album WHERE em_stock=true;")
        for linha in cursor.fetchall():
            print("O valor total de todos os albuns é ", linha[0])

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def valor_vendas():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT sum(valor) FROM compra WHERE finalizada=true;")
        for linha in cursor.fetchall():
            print("O valor total de das vendas é ", linha[0])

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
    
def total_albuns_genero():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        generos_id = []
        generos_nome = []
        total_albuns = 0
        total_exemplares = 0
        cursor.execute("SELECT * FROM genero;")
        for linha in cursor.fetchall():
            generos_id.append(linha[0])
            generos_nome.append(linha[1])

        for i in range(0,len(generos_id)):
            cursor.execute("SELECT * FROM genero_album WHERE genero_id=%s;",(generos_id[i],))
            total_albuns = cursor.rowcount
            cursor.execute("SELECT genero_album.genero_id,genero_album.album_id,album.n_stock FROM genero_album,album WHERE genero_id= %s AND album.id = genero_album.album_id;",(generos_id[i],))
            for linha in cursor.fetchall():
                total_exemplares += linha[2]
            print(generos_nome[i],": ", total_albuns, "Exemplares: ", total_exemplares)
            total_albuns = 0
            total_exemplares = 0
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def total_albuns_editora():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        editora_id = []
        editora_nome = []
        total_albuns = 0
        total_exemplares = 0
        cursor.execute("SELECT * FROM editora;")
        for linha in cursor.fetchall():
            editora_nome.append(linha[0])
            editora_id.append(linha[1])

        for i in range(0,len(editora_id)):
            cursor.execute("SELECT * FROM album WHERE editora_id=%s;",(editora_id[i],))
            total_albuns = cursor.rowcount
            cursor.execute("SELECT n_stock FROM album WHERE editora_id = %s;",(editora_id[i],))
            for linha in cursor.fetchall():
                total_exemplares += linha[0]
            print(editora_nome[i],": ", total_albuns, "Exemplares: ",total_exemplares)
            total_albuns = 0
            total_exemplares = 0
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def albuns_falta_stock():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT nome, id, n_stock FROM album WHERE n_stock<5;")
        if cursor.rowcount == 0:
            print("Não existe nenhum album com falta de stock!")
            return
            
        for linha in cursor.fetchall():
            print("Nome: ",linha[0],"ID: ",linha[1],"Exemplares: ",linha[2])
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def envia_mensagem():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        while True:
            assunto= input("Qual é o assunto da mensagem: ")
            if assunto == '':
                print("Não pode inserir um assunto vazio")
            else:
                break

        while True:
            texto= input("Qual é o texto da mensagem: ")
            if assunto == '':
                print("Não pode inserir um texto vazio")
            else:
                break
        cursor.execute("INSERT INTO mensagem VALUES (nextval('mensagem_id_sequence'),%s,%s,now());",(texto,assunto))
        connection.commit()

        clientes = []
        cursor.execute("SELECT utilizador_email FROM cliente")
        for linha in cursor.fetchall():
            clientes.append(linha[0])
        
        cursor.execute("SELECT id FROM mensagem ORDER BY id DESC LIMIT 1")
        id_mensagem = cursor.fetchone()
        for i in clientes:
            cursor.execute("INSERT INTO leitura VALUES(false,%s,%s);",(id_mensagem[0],i))
            connection.commit()
        
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def mensagem_cliente(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        id_mensagens = []
        print("********************************")
        print("********Caixa de Entrada********")
        print("********************************")
        cursor.execute("SELECT mensagem.id,mensagem.assunto,mensagem.data FROM mensagem,leitura WHERE leitura.lida = false AND leitura.mensagem_id = mensagem.id AND leitura.cliente_utilizador_email = %s;",(user,))
        count = cursor.rowcount
        if count == 0:
            print("Caixa de entrada vazia")
        for linha in cursor.fetchall():
            id = linha[0]
            id_mensagens.append(linha[0])
            assunto = linha[1]
            data = linha[2]
            print("ID: ",id,"Assunto: ",assunto,"Data: ",data)
            print("----------------------------------------")
        print("1. \tLer mensagem")
        print("2. \tLidas")
        print("3. \tMenu inicial")
        while True:
            opcao = input("Insira a opção: ")
            if opcao not in ['1', '2', '3']:
                print("Insira uma opção valida!")
            else:
                break
        if opcao == '1':
            if count == 0:
                print("Não tem mensagens por ler.")
                while True:
                    move_on = input("Enter para continuar")
                    if move_on == '':
                        break
                mensagem_cliente(user)
            else:
                ler_mensagem(user,id_mensagens)
                mensagem_cliente(user)
        if opcao == '2':
            mensagens_n_lidas(user)
            mensagem_cliente(user)
        if opcao == '3':
            menu.menu_cliente(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def mensagens_n_lidas(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        cursor.execute("SELECT mensagem.id,mensagem.assunto,mensagem.data FROM mensagem,leitura WHERE leitura.lida = true AND leitura.mensagem_id = mensagem.id AND leitura.cliente_utilizador_email = %s;",(user,))
        if cursor.rowcount == 0:
            print("Não tem mensagens lidas")
        
        id_mensagens = []

        for linha in cursor.fetchall():
            id = linha[0]
            id_mensagens.append(linha[0])
            assunto = linha[1]
            data = linha[2]
            print("ID: ",id,"Assunto: ",assunto,"Data: ",data)
            print("----------------------------------------")

        while True:
            id = int(input("Insira o id da mensagem que quer ler: "))
            if  id not in id_mensagens:
                print("Não é possivel ler essa mensagem")
            else:
                break
        
        cursor.execute("SELECT assunto,texto FROM mensagem WHERE id = %s;", (id,))

        for linha in cursor.fetchall():
            print("Assunto: ",linha[0])
            print()
            print(linha[1])
            print("---------------FIM------------------------")
        
        while True:
            move_on = input("Enter para continuar")
            if move_on == '':
                break

    except (Exception, psycopg2.Error) as error:
         print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def ler_mensagem(user,id_mensagens):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        while True:
            id = int(input("Insira o id da mensagem que quer ler: "))
            if  id not in id_mensagens:
                print("Não é possivel ler essa mensagem")
            else:
                break
        cursor.execute("SELECT assunto,texto FROM mensagem WHERE id = %s;", (id,))
        for linha in cursor.fetchall():
            print("Assunto: ",linha[0])
            print()
            print(linha[1])
        
        while True:
            move_on = input("Enter para continuar")
            if move_on == '':
                break
        
        cursor.execute("UPDATE leitura SET lida = true WHERE mensagem_id = %s AND cliente_utilizador_email = %s;", (id,user))
        connection.commit()
        count = cursor.rowcount
        #DEBUG
        print(count," record updated succesfully.")

        

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def pesquisa_album(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        op1 = input("Insira o nome do album: ")

        cursor.execute("SELECT id, nome, preco FROM album WHERE nome LIKE '%"+op1+"%' ORDER BY {0} {1};".format(crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            id = linha[0]
            nome = linha[1]
            preco = linha[2]
            print("ID: ",id,"Nome: ",nome,"Preco: ",preco)
        if i == 0:
            print("Não existe nenhum album com esse nome")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def pesquisa_musica(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        op1 = input("Insira o nome da musica: ")
        cursor.execute("SELECT album_id, album.nome, album.id, album.preco "
                       "FROM musica_album "
                       "INNER JOIN album ON musica_album.album_id = album.id "
                       "WHERE musica_id IN (SELECT id FROM musica WHERE nome LIKE '%" + op1 + "%') "
                       "ORDER BY {0} {1}".format(crit, ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            nome = linha[1]
            id = linha[2]
            preco = linha[3]
            print("ID: ", id, "Nome: ", nome, "Preco: ", preco)
        if i == 0:
            print("Não existem albuns com esta música")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def pesquisa_genero(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        op1 = input("Insira o nome do género: ")
        cursor.execute("SELECT album_id, album.nome, album.id, album.preco "
                       "FROM genero_album "
                       "INNER JOIN album ON genero_album.album_id = album.id "
                       "WHERE genero_id IN (SELECT id FROM genero WHERE nome LIKE '%" + op1 + "%') "
                       "ORDER BY {0} {1}".format(crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            nome = linha[1]
            id = linha[2]
            preco = linha[3]
            print("ID: ", id, "Nome: ", nome, "Preco: ", preco)
        if i == 0:
            print("Não existem albuns deste genero")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def pesquisa_artista(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        op1 = input("Insira o nome do artista: ")
        cursor.execute("SELECT album_id, album.nome, album.id, album.preco "
                       "FROM artista_album "
                       "INNER JOIN album ON artista_album.album_id = album.id "
                       "WHERE artista_id IN (SELECT id FROM artista WHERE nome LIKE '%"+op1+"%') "
                        "ORDER BY {0} {1}".format(crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            nome = linha[1]
            id = linha[2]
            preco = linha[3]
            print("ID: ",id,"Nome: ",nome,"Preco: ",preco)
        if i == 0:
            print("Não existem albuns deste artista")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()

def total_preco_genero(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()
        generos_id = []
        generos_nome = []
        total_preco = 0
        cursor.execute("SELECT * FROM genero;")
        for linha in cursor.fetchall():
            generos_id.append(linha[0])
            generos_nome.append(linha[1])

        for i in range(0,len(generos_id)):
            cursor.execute("SELECT * FROM genero_album WHERE genero_id=%s;",(generos_id[i],))
            cursor.execute("SELECT genero_album.genero_id, genero_album.album_id, compra.valor FROM genero_album,compra WHERE genero_id= %s AND compra.album_id = genero_album.album_id AND cliente_utilizador_email = %s ;",(generos_id[i],user))
            for linha in cursor.fetchall():
                total_preco += linha[2]
            if total_preco != 0:
                print("Gastou",total_preco,"€ no genero:",generos_nome[i])
            total_preco = 0
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def pesquisa_artista_historico(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        if crit == 'preco':
            crit = 'valor'

        op1 = input("Insira o nome do artista: ")
        print()
        cursor.execute("SELECT artista_album.album_id, album.nome, compra.id, compra.album_id, compra.data, "
                       "compra.valor, compra.quantidade, compra.data2 FROM artista_album "
                       "INNER JOIN album ON artista_album.album_id=album.id "
                       "INNER JOIN compra ON artista_album.album_id = compra.album_id "
                       "WHERE artista_id IN (SELECT id FROM artista WHERE nome LIKE '%"+op1+"%') "
                       "AND compra.finalizada = true AND cliente_utilizador_email = '{0}' "
                       "ORDER BY {1} {2} ".format(user,crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            album_id = linha[0]
            nome = linha[1]
            id_compra =  linha[2]
            data = linha[4]
            valor = linha[5]
            quant = linha[6]
            data2 = linha[7]
            print("ID da compra: ", id_compra)
            print("ID do album: ", album_id)
            print("Nome do album: ", nome)
            print("Quantidade: ", quant)
            print("Valor: ", valor)
            print("Data em que foi adicionado ao carrinho: ", data)
            print("Data em que foi comprado: ", data2)
            print("-------------------//-------------------------")
        if i == 0:
            print("Não comprou albuns desse artista")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def pesquisa_genero_historico(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        if crit == 'preco':
            crit = 'valor'

        op1 = input("Insira o nome do genero: ")
        print()
        cursor.execute("SELECT genero_album.album_id, album.nome, compra.id, compra.album_id, compra.data, "
                       "compra.valor, compra.quantidade, compra.data2 FROM genero_album "
                       "INNER JOIN album ON genero_album.album_id=album.id "
                       "INNER JOIN compra ON genero_album.album_id = compra.album_id "
                       "WHERE genero_id IN (SELECT id FROM genero WHERE nome LIKE '%"+op1+"%') "
                       "AND compra.finalizada = true AND cliente_utilizador_email = '{0}' "
                       "ORDER BY {1} {2} ".format(user,crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            album_id = linha[0]
            nome = linha[1]
            id_compra =  linha[2]
            data = linha[4]
            valor = linha[5]
            quant = linha[6]
            data2 = linha[7]
            print("ID da compra: ", id_compra)
            print("ID do album: ", album_id)
            print("Nome do album: ", nome)
            print("Quantidade: ", quant)
            print("Valor: ", valor)
            print("Data em que foi adicionado ao carrinho: ", data)
            print("Data em que foi comprado: ", data2)
            print("-------------------//-------------------------")
        if i == 0:
            print("Não comprou albuns deste género")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def pesquisa_musica_historico(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        if crit == 'preco':
            crit = 'valor'

        op1 = input("Insira o nome do musica: ")
        print()
        cursor.execute("SELECT musica_album.album_id, album.nome, compra.id, compra.album_id, compra.data, "
                       "compra.valor, compra.quantidade, compra.data2 FROM musica_album "
                       "INNER JOIN album ON musica_album.album_id=album.id "
                       "INNER JOIN compra ON musica_album.album_id = compra.album_id "
                       "WHERE musica_id IN (SELECT id FROM musica WHERE nome LIKE '%"+op1+"%') "
                       "AND compra.finalizada = true AND cliente_utilizador_email = '{0}' "
                       "ORDER BY {1} {2} ".format(user,crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            album_id = linha[0]
            nome = linha[1]
            id_compra =  linha[2]
            data = linha[4]
            valor = linha[5]
            quant = linha[6]
            data2 = linha[7]
            print("ID da compra: ", id_compra)
            print("ID do album: ", album_id)
            print("Nome do album: ", nome)
            print("Quantidade: ", quant)
            print("Valor: ", valor)
            print("Data em que foi adicionado ao carrinho: ", data)
            print("Data em que foi comprado: ", data2)
            print("-------------------//-------------------------")
        if i == 0:
            print("Não comprou albuns com esta música")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    except (Exception, psycopg2.Error) as error:
        print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()

def pesquisa_album_historico(user,crit,ord):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="localhost",
                                      port="5432",
                                      database="Projecto_BD")

        cursor = connection.cursor()

        if crit == 'preco':
            crit = 'valor'

        op1 = input("Insira o nome do album: ")
        print()
        cursor.execute("SELECT album.id, album.nome, compra.id, compra.data, compra.valor, compra.quantidade, compra.data2 "
                       "FROM album "
                       "INNER JOIN compra ON album.id = compra.album_id "
                       "WHERE album.nome LIKE '%"+op1+"%' "
                       "AND compra.finalizada = true AND cliente_utilizador_email = '{0}' "
                       "ORDER BY album.{1} {2}".format(user,crit,ord))
        i = 0
        for linha in cursor.fetchall():
            i = cursor.rowcount
            album_id = linha[0]
            nome = linha[1]
            id_compra =  linha[2]
            data = linha[4]
            valor = linha[5]
            quant = linha[6]
            data2 = linha[7]
            print("ID da compra: ", id_compra)
            print("ID do album: ", album_id)
            print("Nome do album: ", nome)
            print("Quantidade: ", quant)
            print("Valor: ", valor)
            print("Data em que foi adicionado ao carrinho: ", data)
            print("Data em que foi comprado: ", data2)
            print("-------------------//-------------------------")
        if i == 0:
            print("Não comprou este album")
            menu.menu_cliente(user)
        menu.menu_detalhes(user)

    #except (Exception, psycopg2.Error) as error:
        #print("Error ", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
