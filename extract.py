from datetime import datetime
from decimal import Decimal, InvalidOperation
import logging
import requests 

url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/10?formato=json"

def extrair_dados(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()  
    dados = response.json()
    registros = [] 

    for item in dados:
        data = item['data']
        valor = item['valor']
        registros.append({ "data": data, "valor": valor })

    return registros

def transformar_dados(dados):
    registros_transformados = []

    for registro in dados:
        try:
            data = registro['data']
            valor = registro['valor']
        except KeyError as e:
            logging.error(f"Chave ausente: {e}. Pulando este registro.")
            continue
        try:
            valor = Decimal(valor)
        except InvalidOperation:
            logging.error(f"Valor inválido: {valor}. Pulando este registro.")
            continue
        if not valor.is_finite():
            logging.warning(f"Valor não finito: {valor}. Pulando este registro.")
            continue
        try:
            data = datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            logging.error(f"Data inválida: {data}. Pulando este registro.")
            continue    

        registros_transformados.append({ "data": data, "valor": valor })

    return registros_transformados

if __name__ == "__main__":
    dados = extrair_dados(url)
    registros_transformados = transformar_dados(dados)
    print(registros_transformados)