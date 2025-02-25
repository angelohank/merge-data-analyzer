import os

def log(message):

    log_dir = '/home/angelohank/tmp/merge_analyzer/logs'
    log_file = os.path.join(log_dir, 'execution.log')

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    with open(log_file, 'a') as file:
        file.write(message + '\n')