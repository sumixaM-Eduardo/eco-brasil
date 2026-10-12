from config import DB_HOST, DB_NAME
import psycopg
from datetime import date
from decimal import Decimal
from getpass import getpass

def carregar_dados(conexao, dados):
        with conexao.cursor() as cursor:
            for registro in dados:
                data = registro['data']
                valor = registro['valor']
                cursor.execute("""INSERT INTO selic (data, valor)VALUES (%s, %s)ON CONFLICT (data) DO NOTHING;""", (data, valor))

if __name__ == "__main__":

    usuario = input("Digite o nome do usuário do banco de dados: ")
    senha = getpass("Digite a senha do banco de dados: ")

    with psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=usuario,
        password=senha
    ) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS selic(data DATE PRIMARY KEY, valor NUMERIC NOT NULL);""")
            cursor.execute("""INSERT INTO selic (data, valor)VALUES (%s, %s)ON CONFLICT (data) DO NOTHING;""",(date(2026, 10, 9), Decimal("0.050788")))

