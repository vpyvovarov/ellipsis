from __future__ import unicode_literals
import os
import yaml
from lib.log import get_logger


def load_test_config(config_file='config.yaml'):
    package_root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(package_root, config_file)
    try:
        with open(path) as f:
            config = yaml.load(f)
    except IOError:
        raise RuntimeError("Can't load config at %s" % package_root)
    return config

class Config:
    def __init__(self):
        config = load_test_config()
        self.config = ConfBuilder(config)
        self.log = get_logger(context='Config')

class ConfBuilder:
    def __init__(self, config):
        for key in config:
            value = config[key]
            if issubclass(type(value), dict):
                value = ConfBuilder(value)
            setattr(self, key, value)


if __name__ == "__main__":
    a = Config()