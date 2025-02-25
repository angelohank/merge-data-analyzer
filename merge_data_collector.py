from repository import merge_repository, controle_coleta_repository
from utils import logger
import os
import json
from endpoint import merge_endpoint
from datetime import datetime, timedelta


def get_team(branch_name, data):

    branch_base = branch_name.split('-')[0]
    logger.log(f"MERGE_DATA_COLLECTOR - GET_TEAM [BRANCH_BASE] {branch_base}")

    branches_by_squad = data['branchesBySquad']

    id_team = next((d[branch_name] for d in branches_by_squad if branch_name in d), -1)

    return id_team


def extrair_merges_validos(merges, data):

    logger.log(f"MERGE_DATA_COLLECTOR - EXTRAIR_MERGES_VALIDOS [QT_MERGES] {str(len(merges))}")
    filtered_merges = []

    for merge in merges:
        if 'author' in merge and not merge['author']['username'] in data['ignoreAuthor']:
            if not merge['draft']:
                filtered_merges.append(merge)

    logger.log(f"MERGE_DATA_COLLECTOR - EXTRAIR_MERGES_VALIDOS [QT_MERGES_FILTRADOS] {str(len(filtered_merges))}")
    return filtered_merges


def build_merge_models(merges, data):
    merge_model_list = []
    for merge in merges:
        merge_model = {
            "id": merge['iid'],
            "autor": merge['author']['username'], #TODO construir funcao que anonimiza e ja define a senioridade
            "squad": get_team(merge['source_branch'], data),
            "dt_abertura": merge['created_at'],
            "web_url": merge['web_url'],
            "sha": merge['sha'],
        }

        merge_model_list.append(merge_model)

    return merge_model_list


def process():
    logger.log(f"MERGE_DATA_COLLECTOR - PROCESS")

    path_config = os.path.dirname(os.path.abspath(__file__)) + "/utils/config.json"
    with open(path_config, 'r') as config_file:
        config_file = json.load(config_file)

    data = config_file['data']

    dt_coleta = datetime.now().date()
    coleta = controle_coleta_repository.get_coletas(dt_coleta)

    dt_busca_merges = datetime.now().date()
    if(len(coleta) == 0):
        logger.log(f"MERGE_DATA_COLLECTOR - INSERINDO REGISTRO DE COLETA E BUSCANDO MERGES DE ONTEM")
        controle_coleta_repository.insert_coleta(dt_coleta)

        dt_busca_merges = datetime.now().date() - timedelta(days=1)

    merges = merge_endpoint.get_merges_by_paramns(data, dt_busca_merges)
    logger.log(f"MERGE_DATA_COLLECTOR - PROCESS [QT_MERGES] {str(len(merges))}")

    filtered_merges = extrair_merges_validos(merges, data)
    models = build_merge_models(filtered_merges, data)

    merges_ja_inseridos = merge_repository.get_id_merges()
    merges_to_save = []

    for merge in models:
        if merge['id'] not in merges_ja_inseridos:
            merges_to_save.append(merge)

    merge_repository.inserir_merges(merges_to_save)
    coleta = controle_coleta_repository.get_coletas(dt_coleta)
    controle_coleta_repository.update_primeira_coleta(coleta[0][0])
