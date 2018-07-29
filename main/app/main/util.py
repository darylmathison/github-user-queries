import yaml
import json


class Config:
    """
    This reads a json file and makes the keys the variable names and the
    assigned values as the instance values.  The class is basically
    a layer above a dict class to make the code look cleaner.  The class only
    pulls values from the configuration file and assumes nothing about values.
    The client classes will be assuming the data available.  __getattr__ was
    overloaded to explain what was happening clearer.  __dict__ could have
    been done but readability was chosen.
    """

    def __init__(self, pathname, format_="json"):
        self.config = None
        with open(pathname, "r") as config_file:
            if format_ == "json":
                self._json_to_config(config_file)
            elif format_ == "yaml":
                self._yaml_to_config(config_file)
            else:
                raise ValueError(
                    "{} does not support the {} format".format(
                        self.__class__, format_)
                )

    def _json_to_config(self, config_file):
        self.config = json.load(config_file)

    def _yaml_to_config(self, config_file):
         self.config = yaml.load(config_file)

    def __getattr__(self, item):
        if isinstance(item, slice):
            raise AttributeError(
                "{} does not support slices".format(self.__class__)
            )

        if item in self.config:
            return self.config[item]
        elif item in self.__dict__:
            return self.__dict__[item]
        else:
            raise AttributeError("{} is not an attribute".format(item))
