from configparser import ConfigParser


def read_config(filename='config.ini'):
    config = ConfigParser()
    config.read(filename)
    return config


def get_config_value(config, section, option):
    return config.get(section, option)


def get_config_int_value(config, section, option):
    return config.getint(section, option)
