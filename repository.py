import sys

import psycopg2
import os
import json
from psycopg2._psycopg import cursor

import logger

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
def inserir_merge(merge_list):
    connection = connection_db()

    if connection is None:
        logger.log("Erro ao conectar no banco de dados")
        return

    try:
        cursor = connection.cursor()

        #TODO inserir conjunto atual
        insert_query = """
        INSERT INTO merges (id_merge, autor, squad, dt_abertura, size_conjunto_atual, link, sha)
        VALUES (%s, %s, %s, %s, 0, %s, %s)
        """

        for merge in merge_list:
            cursor.execute(insert_query, (
                merge['id'],
                merge['autor'],
                merge['squad'],
                merge['dt_abertura'],
                merge['web_url'],
                merge['sha']
            ))

        connection.commit()
        logger.log("Numero de linhas afetadas: " + str(cursor.rowcount))

    except Exception as e:
        logger.log(f"Erro ao inserir dados: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

def inserir_pipeline(pipelines):
    logger.log("Inseriring pipelines")
    print("inserindo pipelines")
    connection = connection_db()

    if connection is None:
        logger.log("Erro ao conectar no banco de dados")
        return

    try:
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO pipelines (id_pipeline, id_merge, qtd_falhos, sha, iid, status, link)
            VALUES (%s, %s, 0, %s, %s, %s, %s)
            """

        for pipeline in pipelines:
            cursor.execute(insert_query, (
                pipeline['id_pipeline'],
                pipeline['id_merge'],
                pipeline['sha'],
                pipeline['iid'],
                pipeline['status'],
                pipeline['link']
            ))

        connection.commit()
        print(str(cursor.rowcount))
        logger.log("inserir_pipeline [Numero de linhas afetadas] " + str(cursor.rowcount))

    except Exception as e:
        logger.log(f"Erro ao inserir dados: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

def get_id_pipelines():
    connection = connection_db()

    if connection is None:
        logger.log("get_id_pipelines - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()

        # TODO passar um parametro para filtrar e nao trazer todos os merges sempre
        query = "SELECT id_pipeline FROM pipelines"

        cursor.execute(query)

        ids_pipelines = cursor.fetchall()

        return [id[0] for id in ids_pipelines]


    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"get_id_pipelines - Erro ao acessar o banco de dados: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_id_merges():
    connection = connection_db()

    if connection is None:
        logger.log("get_id_merges - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()

        #TODO passar um parametro para filtrar e nao trazer todos os merges sempre
        query = "SELECT id_merge FROM merges"

        cursor.execute(query)

        ids_merge = cursor.fetchall()

        return [id[0] for id in ids_merge]


    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"Erro ao acessar o banco de dados: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()
