import psycopg2
from utils import logger
from utils.repository import connection_db

def update_pipeline_data_by_report(report):
    connection = connection_db()

    if connection is None:
        logger.log("PIPELINE_REPOSITORY - UPDATE_PIPELINE_DATA_BY_REPORT - Erro ao conectar no banco de dados")
        return

    try:
        cursor = connection.cursor()

        insert_query = """
                UPDATE pipelines SET qtd_falhos = %s, size_conjunto_atual = %s, fgdadoscoletados = 'T' WHERE id_pipeline = %s
                """

        #TODO remover numeros magicos
        cursor.execute(insert_query, (
            report[0],
            report[1],
            report[2]
        ))

        connection.commit()
        logger.log("PIPELINE_REPOSITORY - UPDATE_PIPELINE_DATA_BY_REPORT [ROW_COUNT] " + str(cursor.rowcount))

    except Exception as e:
        logger.log(f"PIPELINE_REPOSITORY - UPDATE_PIPELINE_DATA_BY_REPORT [WHAT] {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()


def get_pipelines_a_verificar():
    connection = connection_db()

    if connection is None:
        logger.log("get_pipelines_a_verificar - Erro ao conectar ao banco de dados")
        return

    try:
        cursor = connection.cursor()

        query = "SELECT id_pipeline FROM pipelines where fgdadoscoletados = 'F'"

        cursor.execute(query)

        pipelines = cursor.fetchall()

        return [id[0] for id in pipelines]


    except (Exception, psycopg2.DatabaseError) as e:
        logger.log(f"Erro ao acessar o banco de dados: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()


def inserir_pipeline(pipelines):
    logger.log("Inseriring pipelines")
    connection = connection_db()

    if connection is None:
        logger.log("Erro ao conectar no banco de dados")
        return

    try:
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO pipelines (id_pipeline, id_merge, qtd_falhos, sha, iid, status, link, size_conjunto_atual)
            VALUES (%s, %s, 0, %s, %s, %s, %s, %s)
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
        logger.log("inserir_pipeline [Numero de linhas afetadas] " + str(cursor.rowcount))

    except Exception as e:
        logger.log(f"inserir_pipeline - Erro ao inserir dados: {e}")
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

def gravar_pipelines(pipelines):
    logger.log(f"PIPELINE_REPOSITORY - GRAVAR_PIPELINES [QT_PIPELINES] {str(len(pipelines))}")

    connection = connection_db()
    if connection is None:
        logger.log("PIPELINE_REPOSITORY - GRAVAR_PIPELINES - Erro ao conectar no banco de dados")
        return
    try:
        cursor = connection.cursor()

        insert_query = """
                INSERT INTO pipelines (id_pipeline, id_merge, sha, iid, link)
                VALUES (%s, %s, %s, %s, %s)
                """

        for pipeline in pipelines:
            cursor.execute(insert_query, (
                pipeline['id_pipeline'],
                pipeline['id_merge'],
                pipeline['sha'],
                pipeline['iid'],
                pipeline['link']
            ))

        connection.commit()
        logger.log("PIPELINE_REPOSITORY - GRAVAR_PIPELINES [ROW_COUNT] " + str(cursor.rowcount))
    except Exception as e:
        logger.log(f"PIPELINE_REPOSITORY - GRAVAR_PIPELINES [WHAT] {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()