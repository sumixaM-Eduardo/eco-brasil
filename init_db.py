import psycopg
import getpass
from config import DB_HOST, DB_NAME, DB_PORT
import logging

def criar_banco():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    usuario = input("Digite o nome do usuário do banco de dados: ")
    senha = getpass.getpass("Digite a senha do banco de dados: ")
    
    try:
        with psycopg.connect(
            host=DB_HOST,
            dbname="postgres",
            port=DB_PORT,
            user=usuario, 
            password=senha,
            autocommit=True
        ) as conexao_admin:
            with conexao_admin.cursor() as cursor:
                cursor.execute("""SELECT 1 FROM pg_database WHERE datname = %s""", (DB_NAME,))
                if cursor.fetchone() is None:
                    cursor.execute(psycopg.sql.SQL("""CREATE DATABASE {}""").format(psycopg.sql.Identifier(DB_NAME)))
                    logging.info(f"Banco de dados '{DB_NAME}' criado com sucesso.")
                else:
                    logging.info(f"Banco de dados '{DB_NAME}' já existe.")

        with psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            port=DB_PORT,
            user=usuario,
            password=senha
        ) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS selic (data DATE PRIMARY KEY,valor NUMERIC NOT NULL);""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS observacoes (serie_id INTEGER NOT NULL,
                  data DATE NOT NULL, valor NUMERIC NOT NULL,
                    PRIMARY KEY (serie_id, data));""")
                
        logging.info("Tabelas criadas ou já existentes.")
    except psycopg.Error as error:
        logging.error(f"Erro ao criar banco de dados e tabelas: {error}")
        raise
