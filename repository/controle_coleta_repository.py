from utils.repository import connection_db
from utils import logger
import psycopg2

def get_coletas(dt_coleta):
    connection = connection_db()
    if connection is None:
        logger.log(f"MERGE_REPOSITORY - GET_COLETAS - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()
        query = "SELECT id_controle_coleta, primeira_coleta, dt_coleta FROM controle_coleta WHERE dt_coleta = %s"

        cursor.execute(query, (dt_coleta,))
        coleta = cursor.fetchall()

        return coleta

    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - GET_COLETAS - Erro ao acessar o banco de dados [WHAT] {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()


def insert_coleta(dt_coleta):
    connection = connection_db()
    if connection is None:
        logger.log(f"MERGE_REPOSITORY - INSERT_COLETA - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()
        query = "INSERT INTO controle_coleta (dt_coleta) VALUES (%s)"

        cursor.execute(query, (dt_coleta,))
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - INSERT_COLETA - Erro ao acessar o banco de dados [WHAT] {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()


def update_primeira_coleta(id_controle_coleta):
    connection = connection_db()
    if connection is None:
        logger.log(f"MERGE_REPOSITORY - UPDATE_PRIMEIRA_COLETA - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()
        query = "UPDATE controle_coleta SET primeira_coleta = 'T' WHERE id_controle_coleta = %s"

        cursor.execute(query, (id_controle_coleta,))
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - UPDATE_PRIMEIRA_COLETA - Erro ao acessar o banco de dados [WHAT] {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()