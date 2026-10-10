import psycopg
from getpass import getpass

usuario = input("Digite o nome do usuário do banco de dados: ")
senha = getpass("Digite a senha do banco de dados: ")

with psycopg.connect(
    host="localhost",
    dbname="ecobrasil",
    user=usuario,
    password=senha
) as conexao:
    with conexao.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS selic(data DATE PRIMARY KEY, valor NUMERIC NOT NULL);""")
    print("Tabela selic criada ou já existente.")