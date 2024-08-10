import requests


def get_data(config):
    DATA = config['data']

    PRIVATE_TOKEN = DATA['privateToken']
    API_URL = DATA['apiUrl']
    PROJECT_ID = DATA['projectId']
    PER_PAGE = DATA['perPage']
    MERGE_CONFIG = config['merge']
    CREATED_AFTER = MERGE_CONFIG['createdAfter']
    CREATED_BEFORE = MERGE_CONFIG['createdBefore']

    # TODO transformar esses caras em uma lista
    MERGE_STATE = MERGE_CONFIG['state']
    IGNORE_AUTHOR = MERGE_CONFIG['ignoreAuthor']
    TEAMS = DATA['teams']
    BRANCH_PREFIX_PATTERN = DATA['branchPrefixPattern']

    url = f"{API_URL}/projects/{PROJECT_ID}/merge_requests"
    header = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

    all_merges = []

    print("Buscando merges realizados entre as datas determinadas")

    page = 1
    while True:
        params = {
            "created_after": CREATED_AFTER,
            "created_before": CREATED_BEFORE,
            "page": page,
            "per_page": PER_PAGE,
            "state": MERGE_STATE
        }

        response = requests.get(url, params=params, headers=header)

        if response.status_code == 200:
            data = response.json()
            for merge in data:
                merge_user_data = merge['merge_user']

                if merge_user_data is not None:
                    username = merge_user_data['username']
                    if not username == IGNORE_AUTHOR:
                        all_merges.append(merge)

        if 'next' not in response.links:
            break

        page += 1

    for team in TEAMS:
        get_merges_by_team(BRANCH_PREFIX_PATTERN, team, all_merges)


def get_merges_by_team(branch_prefix_pattern, team_name, data):
    print("buscando merges do time " + team_name)

    branch_team = branch_prefix_pattern + team_name
    merges_team = []

    for merge in data:
        merge_branch = merge['source_branch']
        if merge_branch.startswith(branch_team):
            merges_team.append(merge)

    print(len(merges_team))

