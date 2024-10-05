import requests
import repository
import logger
from datetime import datetime, timedelta

def get_data(config):
    search_params = config['data']

    private_token = search_params['privateToken']
    api_url = search_params['apiUrl']
    project_id = search_params['projectId']
    per_page = search_params['perPage']
    state = search_params['state']

    url = f"{api_url}/projects/{project_id}/merge_requests"
    header = {"PRIVATE-TOKEN": private_token}

    params = {
        "per_page": per_page,
        "state": state
    }

    logger.log(f"Buscando merges [DT_BUSCA] {(datetime.now()).isoformat()}")

    response = requests.get(url, params=params, headers=header)

    if response.status_code != 200:
        logger.log(f"Error ao buscar merges [STATUS CODE] {str(response.status_code)}")
        return

    data = response.json()

    filtered_merges = []
    valid_merges = filtered_merges_by_author(search_params, data)

    for merge in filtered_merges_by_squad(search_params['teams'][0], valid_merges, search_params['branchPrefixPattern']):
        filtered_merges.append(merge)

    for merge in filtered_merges_by_squad(search_params['teams'][1], valid_merges, search_params['branchPrefixPattern']):
        filtered_merges.append(merge)

    for merge in get_merges_by_general_branchs(search_params['generalBranchs'], valid_merges):
        filtered_merges.append(merge)

    print(filtered_merges)
    merge_dto_list = []

    merges_mapped = repository.get_id_merges()

    for merge in filtered_merges:
        merge_dto = {
            "id": merge['iid'],
            "autor": merge['author']['username'],
            "squad": get_team(merge['source_branch']),
            "dt_abertura": merge['created_at'],
            "web_url": merge['web_url'],
            "sha": merge['sha']
        }

        if merge_dto['id'] not in merges_mapped:
            merge_dto_list.append(merge_dto)

    repository.inserir_merge(merge_dto_list)

def filtered_merges_by_author(config, data):
    filtered_merges = []

    for merge in data:

        #eliminando autores nao desejados
        if 'author' in merge and not merge['author']['username'] in config['ignoreAuthor']:
            filtered_merges.append(merge)

    return filtered_merges


def filtered_merges_by_squad(team_name, merges, branch_prefix_pattern):
    merges_by_team = []

    prefix_branch = branch_prefix_pattern + team_name

    for merge in merges:
        if merge['source_branch'].startswith(prefix_branch):
            merges_by_team.append(merge)

    return merges_by_team


#TODO dar um jeito de deixar isso mais generico
def get_merges_by_general_branchs(general_branchs, merges):
    general_merges = []

    for merge in merges:
        if merge['source_branch'] in general_branchs and not merge['draft']:
            general_merges.append(merge)

    return general_merges

def get_team(branch_name):
    #TODO pegar do arquivo de configuracao
    if branch_name.startswith('build/echo'):
        return 0

    return 1

