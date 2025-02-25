import os
import json

LOG_PATH = None

def prepare_log_directory(path):
    os.makedirs(path, exist_ok=True)
    log_file = os.path.join(path, "execution.log")
    if not os.path.exists(log_file):
        open(log_file, "w").close()


def get_log_output_path():
    global LOG_PATH
    if LOG_PATH is None:
        with open("./utils/config.json", "r") as f:
            config = json.load(f)

        LOG_PATH = config.get("log_path", "./logs")
        prepare_log_directory(LOG_PATH)
    return LOG_PATH


def log(message):

    path_config = os.path.dirname(os.path.abspath(__file__)) + "/utils/config.json"
    with open(path_config, 'r') as config_file:
        config_file = json.load(config_file)

    log_path = get_log_output_path()
    log_file = os.path.join(log_path, 'execution.log')

    with open(log_file, 'a') as file:
        file.write(message + '\n')