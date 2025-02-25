from utils import logger
import requests

ENDPOINT = 'pipelines'

def get_pipeline_by_sha(sha, config):
    logger.log(f"PIPELINE_ENDPOINT - GET_PIPELINE_BY_SHA")

    private_token = config['privateToken']
    api_url = config['apiUrl']
    project_id = config['projectId']

    url = f"{api_url}/projects/{project_id}/{ENDPOINT}"
    params = {
        'sha': sha
    }
    header = {"PRIVATE-TOKEN": private_token}

    response = requests.get(url, params=params, headers=header)

    if response.status_code != 200:
        logger.log(f"PIPELINE_ENDPOINT - GET_PIPELINE_BY_SHA [STATUS CODE] {str(response.status_code)}")
        return

    data = response.json()

    return data


def check_pipeline_tests_done(id_pipeline, config):
    logger.log(f"PIPELINE_ENDPOINT - CHECK_PIPELINE_ARRIVED_AT_TESTS [ID_PIPELINE] {id_pipeline}")

    private_token = config['privateToken']
    api_url = config['apiUrl']
    project_id = config['projectId']
    headers = {
        'PRIVATE-TOKEN': private_token
    }

    url = f"{api_url}/projects/{project_id}/{ENDPOINT}/{id_pipeline}/jobs"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        test_jobs = []
        for job in data:
            if job['stage'] == 'test':
                test_jobs.append(job)

        for job in test_jobs:
            if job.get('status') in ['failed', 'success']:
                return True

    return False
