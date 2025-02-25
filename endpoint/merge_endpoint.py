from datetime import datetime
import requests
import os
import json

from utils import logger

ENDPOINT = 'merge_requests'

def get_merges_by_paramns(config, dt_busca):
    logger.log(f"MERGE_ENDPOINT - GET_MERGES_BY_PARAMNS")

    private_token = config['privateToken']
    api_url = config['apiUrl']
    project_id = config['projectId']
    per_page = config['perPage']
    state = config['state']

    url = f"{api_url}/projects/{project_id}/{ENDPOINT}"
    header = {"PRIVATE-TOKEN": private_token}

    params = {
        "per_page": per_page,
        "state": state,
        "created_after": dt_busca
    }

    logger.log(f"MERGE_ENDPOINT - GET_MERGES_BY_PARAMNS [DT_BUSCA] {datetime.now().replace(hour=0, minute=0, second=0).isoformat()}")

    response = requests.get(url, params=params, headers=header)

    if response.status_code != 200:
        logger.log(f"MERGE_ENDPOINT - GET_MERGES_BY_PARAMNS [STATUS CODE] {str(response.status_code)}")
        return

    data = response.json()

    return data