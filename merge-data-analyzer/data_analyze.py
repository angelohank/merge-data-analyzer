import json
import requests

def get_data(config):
    DATA = config['data']

    PRIVATE_TOKEN = DATA['privateToken']
    API_URL = DATA['apiUrl']
    PROJECT_ID = DATA['projectId']

    MERGE_CONFIG = config['merge']
    CREATED_AFTER = MERGE_CONFIG['createdAfter']
    CREATED_BEFORE = MERGE_CONFIG['createdBefore']
    MERGE_STATE = MERGE_CONFIG['state']


    url = f"{API_URL}/projects/{PROJECT_ID}/merge_requests"
    header = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    params = {
        "created_after": CREATED_AFTER,
        "created_before": CREATED_BEFORE,
        "state": MERGE_STATE
    }

    response = requests.get(url, params=params, headers=header)
    print(response.status_code)
    print(response.json())
