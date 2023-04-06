"""
Модуль для работы с файлом конфигурации.
"""

import yaml


def open_config():
    with open('config.yaml') as config_file:
        config = yaml.safe_load(config_file)
    return config


if __name__ == "__main__":
    config = open_config()
    print(config["video"]["path"])
