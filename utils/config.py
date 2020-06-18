## -------------- IMPORT --------------
import os
import yaml
## ----------- LOCAL IMPORT -----------
from .logger import Logger
## ------------- CONSTANT -------------
SEPARATOR = "__"
logger = Logger(os.path.basename(__file__))

def flatten_dict(dd, separator=SEPARATOR, prefix=''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }


class Config_Reader:
    """
    Class that read the value of a config file.
    """
    instance_config = None
    name_file = "config.yml"
    @classmethod
    def get(self, index, name_file=name_file):
        if Config_Reader.instance_config is None:
            Config_Reader.instance_config = Config(name_file=name_file)

        return Config_Reader.instance_config.get_config_value(index)


class Config:
    def __init__(self, path_config=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), name_file="config.yml"):
        print(os.path.join(path_config, name_file))
        if not os.path.isfile(os.path.join(path_config, name_file)):
            raise Exception("Config file does not exist")

        self.config_key_path = {}
        with open(os.path.join(path_config, name_file), 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        flat_dict = flatten_dict(cfg)
        for key, value in flat_dict.items():
            path = key.split(SEPARATOR)
            if path[-1] in self.config_key_path:
                logger.warning("two identical value has been found in the config file.")
            self.config_key_path[path[-1]] = {"value": value, "path": path[:-1]}

    def get_config_value(self, index):
        if index is None:
            raise Exception("Config key should not be None")

        if index not in self.config_key_path:
            logger.error("Key -- {key} -- not present in the config file".format(key=index))
            raise Exception("Key -- {key} -- not present in the config file".format(key=index))
        return self.config_key_path[index]["value"]

