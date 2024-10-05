import os
import json

def log(message):
    path_config = os.path.dirname(os.path.abspath(__file__)) + "/config.json"

    with open(path_config, 'r') as config_file:
        config_file = json.load(config_file)

    log_dir = config_file["log_dir"]
    log_file = os.path.join(log_dir, 'execution.log')

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    with open(log_file, 'a') as file:
        file.write(message + '\n')