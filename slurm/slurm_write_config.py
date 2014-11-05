import os


def write_config_file(job_name, config_param):

    commands_filename = os.path.join(job_name + "_config.txt")
    commands_file = open(commands_filename, 'w')
    commands_file.writelines(config_param)
    commands_file.close()