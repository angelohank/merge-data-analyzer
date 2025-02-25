from utils.repository import connection_db
from utils import logger
import psycopg2

def inserir_merges(merge_list):
    logger.log(f"MERGE_REPOSITORY - INSERIR_MERGES [QT_MERGES] {str(len(merge_list))}")
    connection = connection_db()

    if connection is None:
        logger.log("MERGE_REPOSITORY - INSERIR_MERGES Erro ao conectar no banco de dados")
        return

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO merges (id_merge, autor, squad, dt_abertura, link, sha)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        for merge in merge_list:
            cursor.execute(query, (
                merge['id'],
                merge['autor'],
                merge['squad'],
                merge['dt_abertura'],
                merge['web_url'],
                merge['sha']
            ))

        connection.commit()
        logger.log("MERGE_REPOSITORY - INSERIR_MERGES [ROWS_COUNT] " + str(cursor.rowcount))

    except Exception as e:
        logger.log(f"MERGE_REPOSITORY - INSERIR_MERGES - Erro ao inserir dados [WHAT] {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()


def get_id_merges():
    connection = connection_db()

    if connection is None:
        logger.log("MERGE_REPOSITORY - GET_ID_MERGES - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()

        #TODO passar um parametro para filtrar e nao trazer todos os merges sempre
        query = "SELECT id_merge FROM merges"

        cursor.execute(query)

        ids_merge = cursor.fetchall()

        return [id[0] for id in ids_merge]


    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - GET_ID_MERGES - Erro ao acessar o banco de dados [WHAT] {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()

def get_merges_nao_coletados():
    connection = connection_db()

    if connection is None:
        logger.log("MERGE_REPOSITORY - GET_MERGES_NAO_COLETADOS - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()

        query = "SELECT id_merge, sha FROM merges where fgrevisado = 'F'"

        cursor.execute(query)

        merges = cursor.fetchall()

        return [{'id_merge': merge[0], 'sha': merge[1]} for merge in merges ]

    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - GET_MERGES_NAO_COLETADOS - Erro ao acessar o banco de dados [WHAT] {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()

def update_fg_revisado_by_pipeline_sha(pipelines):
    logger.log(f"MERGE_REPOSITORY - UPDATE_FG_REVISADO_BY_PIPELINE_SHA [QT_PIPELINES] {str(len(pipelines))}")

    connection = connection_db()
    if connection is None:
        logger.log("MERGE_REPOSITORY - UPDATE_FG_REVISADO_BY_PIPELINE_SHA - Erro ao conectar ao banco de dados")
        return
    try:
        cursor = connection.cursor()
        query = "UPDATE merges SET fgrevisado = 'T' WHERE sha = %s"

        for pipeline in pipelines:
            cursor.execute(query, (
                pipeline['sha'],
            ))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - UPDATE_FG_REVISADO_BY_PIPELINE_SHA - Erro ao acessar o banco de dados [WHAT] {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def delete_merge_by_id(id_merge):
    logger.log(f"MERGE_REPOSITORY - DELETE_MERGE_BY_ID [ID_MERGE] {str(id_merge)}")

    connection = connection_db()
    if connection is None:
        logger.log("MERGE_REPOSITORY - DELETE_MERGE_BY_ID - Erro ao conectar ao banco de dados")
        return
    try:
        cursor = connection.cursor()
        query = "DELETE FROM merges WHERE id_merge = %s"
        cursor.execute(query, (id_merge,))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"MERGE_REPOSITORY - DELETE_MERGE_BY_ID - Erro ao acessar o banco de dados [WHAT] {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()