import json


_config = None


def get_config():
    """ get the config json data """
    global _config

    if _config:
        return _config
    _config = json.loads(open('config.json').read())
    return _config
