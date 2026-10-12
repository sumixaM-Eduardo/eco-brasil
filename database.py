from config import DB_HOST, DB_NAME
import psycopg
from datetime import date
from getpass import getpass

def carregar_dados(conexao, dados):
    inseridos = 0

    with conexao.cursor() as cursor:
        for registro in dados:
            data = registro['data']
            valor = registro['valor']
            cursor.execute("""INSERT INTO selic (data, valor)VALUES (%s, %s)ON CONFLICT (data) DO NOTHING;""", (data, valor))
            inseridos += cursor.rowcount
    return inseridos
        