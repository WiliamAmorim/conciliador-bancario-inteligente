import os
import logging
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

logger = logging.getLogger(__name__)


def obter_conexao():
    try:
        logger.info("Iniciando conexão com o banco de dados...")

        # 🔎 Validar variáveis obrigatórias
        db_config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

        for chave, valor in db_config.items():
            if not valor:
                raise ValueError(f"Variável de ambiente ausente: {chave}")

        conexao = mysql.connector.connect(**db_config)

        if conexao.is_connected():
            logger.info("Conexão com o banco estabelecida com sucesso.")

        return conexao

    except ValueError as ve:
        logger.critical(f"Erro de configuração: {ve}")
        raise

    except Error as db_error:
        logger.error(f"Erro ao conectar no MySQL: {db_error}")
        raise

    except Exception as e:
        logger.exception("Erro inesperado ao obter conexão.")
        raise