from repository import pipeline_repository, teste_falha_repository
from utils import logger
from endpoint import test_report_endpoint
import os
import json

def extract_data_from_report(report, id_pipeline):
    logger.log(f"TEST_REPORT_DATA_COLLECTOR - PROCESS [ID_PIPELINE] {id_pipeline}")

    failed_tests = []
    total_failed_count = report['failed_count']
    total_tests_count = report['total_count']

    for test_suite in report.get('test_suites', []):
        for case in test_suite.get('test_cases', []):
            if case['status'] == 'failed':
                failed_tests.append(case['name'])

    logger.log(f"TEST_REPORT_DATA_COLLECTOR - EXTRACT_DATA_FROM_REPORT [QT_TESTES_FALHOS] {str(total_failed_count)} [QT_TOTAL_TESTS] {str(total_tests_count)}")

    ds_testes_falhos = []
    for test in failed_tests:
        ds_testes_falhos.append(test)

    return total_failed_count, total_tests_count, id_pipeline, ds_testes_falhos


def process():
    pipelines_a_verificar = pipeline_repository.get_pipelines_a_verificar()
    logger.log(f"TEST_REPORT_DATA_COLLECTOR - PROCESS [QT_PIPELINES] {str(len(pipelines_a_verificar))}")

    path_config = os.path.dirname(os.path.abspath(__file__)) + "/utils/config.json"

    with open(path_config, 'r') as config_file:
        config_file = json.load(config_file)

    data = config_file['data']

    for id_pipeline in pipelines_a_verificar:
        report = test_report_endpoint.get_test_report_by_pipeline(id_pipeline, data)

        data_from_report = extract_data_from_report(report, id_pipeline)

        pipeline_repository.update_pipeline_data_by_report(data_from_report)
        teste_falha_repository.inserir_testes_falhos(data_from_report)

