from endpoint import pipeline_endpoint
from repository import pipeline_repository, merge_repository
from utils import logger
import os
import json

def process():
    logger.log(f"PIPELINE_DATA_COLLECTOR - PROCESS")

    path_config = os.path.dirname(os.path.abspath(__file__)) + "/utils/config.json"
    with open(path_config, 'r') as config_file:
        config_file = json.load(config_file)

    data = config_file['data']

    get_merges_sha = merge_repository.get_merges_nao_coletados()
    logger.log(f"PIPELINE_DATA_COLLECTOR - PROCESS [QT_MERGES_NAO_COLETADOS] {str(len(get_merges_sha))}")

    pipelines_to_save = []
    pipeline_model_list = []
    for merge in get_merges_sha:
        sha = merge['sha']

        response = pipeline_endpoint.get_pipeline_by_sha(sha, data)

        for pipeline in response:
            pipeline_model = {
                "id_pipeline": pipeline['id'],
                "iid": pipeline['iid'],
                "sha": pipeline['sha'],
                "link": pipeline['web_url'],
                "id_merge": merge['id_merge']
            }

            pipeline_model_list.append(pipeline_model)

            break

    pipelines_ja_inseridas = pipeline_repository.get_id_pipelines()
    for pipeline in pipeline_model_list:
        if pipeline['id_pipeline'] not in pipelines_ja_inseridas:
            ran_all_tests = pipeline_endpoint.check_pipeline_tests_done(pipeline['id_pipeline'], config_file['data'])
            logger.log(f"PIPELINE_DATA_COLLECTOR - PROCESS [ID_PIPELINE] {pipeline['id_pipeline']}"
                       f" [RAN_ALL_TESTS] {ran_all_tests}")
            if ran_all_tests:
                pipelines_to_save.append(pipeline)
            else:
                logger.log(f"PIPELINE_DATA_COLLECTOR - PROCESS")
                merge_repository.delete_merge_by_id(pipeline['id_merge'])

    pipeline_repository.gravar_pipelines(pipelines_to_save)
    merge_repository.update_fg_revisado_by_pipeline_sha(pipelines_to_save)