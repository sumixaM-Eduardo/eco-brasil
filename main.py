import psycopg
import requests
from config import DB_HOST, DB_NAME
from getpass import getpass
from extract import extrair_dados, transformar_dados, url
from database import carregar_dados


if __name__ == "__main__":
    try:
        dados = extrair_dados(url)
    except requests.RequestException as error:
        print(f"Erro ao consultar a API: {error}")
        raise SystemExit(1)
    
    registros_transformados = transformar_dados(dados)

    print(f"Registros válidos: {len(registros_transformados)}")

    usuario = input("Digite o nome do usuário do banco de dados: ")
    senha = getpass("Digite a senha do banco de dados: ")

    with psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=usuario,
        password=senha
    ) as conexao:
        carregar_dados(conexao, registros_transformados)

    print("Carga concluída.")