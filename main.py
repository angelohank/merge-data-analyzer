import os.path
import json
import data_analyze

if __name__ == "__main__":
    path_config = os.path.dirname(os.path.abspath(__file__)) + "/config.json"

    with open(path_config, 'r') as config_file:
        config_file = json.load(config_file)

data_analyze.get_data(config_file)