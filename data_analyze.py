from utils import logger
import merge_data_collector
import pipeline_data_collector
import test_report_data_collector

def get_data():
    logger.log(f"DATA_ANALYZER - GET_DATA")

    merge_data_collector.process()
    pipeline_data_collector.process()
    test_report_data_collector.process()

