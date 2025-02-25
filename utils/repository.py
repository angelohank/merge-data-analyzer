import psycopg2
import os
import json

from utils import logger


def connection_db():
    path_config = os.path.dirname(os.path.abspath(__file__)) + "/config_db.json"

    with open(path_config, 'r') as config_file:
        config = json.load(config_file)

    try:
        connection = psycopg2.connect(
            dbname=config['database_name'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
        return connection
    except Exception as e:
        logger.log(f"Erro ao conectar ao banco de dados: {e}")
        return None