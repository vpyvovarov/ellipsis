from __future__ import unicode_literals
import os
import yaml


def load_test_config(config_file='config.yaml'):
    package_root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(package_root, config_file)
    try:
        with open(path) as f:
            config = yaml.load(f)
    except IOError:
        config = None
    return config


class Config:
    def __init__(self):
        config = load_test_config()
        for key in config:
            setattr(self, key, config[key])
