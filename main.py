import psycopg
import logging
import requests
from config import DB_HOST, DB_NAME
from getpass import getpass
from extract import extrair_dados, transformar_dados, url
from database import carregar_dados
from init_db import criar_banco

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    usuario = input("Digite o nome do usuário do banco de dados: ")
    senha = getpass("Digite a senha do banco de dados: ")

    criar_banco(usuario, senha)

    try:
        dados = extrair_dados(url)
    except requests.RequestException as error:
        logging.error(f"Erro ao consultar a API: {error}")
        raise SystemExit(1)
    
    registros_transformados = transformar_dados(dados)

    logging.info(f"Registros válidos: {len(registros_transformados)}")

    try:
        with psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=usuario,
            password=senha
        ) as conexao:
            inseridos = carregar_dados(conexao, registros_transformados)
    except psycopg.Error as error:
        logging.error(f"Erro ao conectar ou inserir dados no banco de dados: {error}")
        raise SystemExit(1)

    ignorados = len(registros_transformados) - inseridos

    logging.info(f"Carga concluida: {inseridos} inseridos, {ignorados} já existentes.")