import requests
from utils import logger
import os
import json

ENDPOINT = 'test_report'

def get_test_report_by_pipeline(id_pipeline, config):
    logger.log(f"TEST_REPORT_ENDOINT - GET_TEST_REPORT_BY_PIPELINE [PIPELINE_ID] {id_pipeline}")

    private_token = config['privateToken']
    api_url = config['apiUrl']
    project_id = config['projectId']
    header = {"PRIVATE-TOKEN": private_token}

    url = f"{api_url}/projects/{project_id}/pipelines/{id_pipeline}/{ENDPOINT}"

    response = requests.get(url, headers=header)
    data = response.json()

    return data
