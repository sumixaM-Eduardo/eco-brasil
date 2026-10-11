import psycopg
from getpass import getpass

from extract import extrair_dados, transformar_dados, url
from database import carregar_dados


if __name__ == "__main__":
    dados = extrair_dados(url)
    registros_transformados = transformar_dados(dados)

    print(f"Registros válidos: {len(registros_transformados)}")

    usuario = input("Digite o nome do usuário do banco de dados: ")
    senha = getpass("Digite a senha do banco de dados: ")

    with psycopg.connect(
        host="localhost",
        dbname="ecobrasil",
        user=usuario,
        password=senha
    ) as conexao:
        carregar_dados(conexao, registros_transformados)

    print("Carga concluída.")