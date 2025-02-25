from utils.repository import connection_db
from utils import logger

def inserir_testes_falhos(report):
    connection = connection_db()
    if connection is None:
        logger.log("TESTE_FALHA_REPOSITORY - INSERIR_TESTES_FALHOS - Erro ao conectar no banco de dados")
        return

    try:
        cursor = connection.cursor()

        insert_query = """
                    INSERT INTO teste_unidade_falha (desc_teste, id_pipeline) VALUES (%s, %s)
                    """

        #TODO remover numeros magicos
        for ds_test in report[3]:
            cursor.execute(insert_query, (
                ds_test,
                report[2]
            ))

        connection.commit()
        logger.log("TESTE_FALHA_REPOSITORY - INSERIR_TESTES_FALHOS [ROW_COUNT] " + str(cursor.rowcount))

    except Exception as e:
        logger.log(f"TESTE_FALHA_REPOSITORY - INSERIR_TESTES_FALHOS [WHAT] {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
