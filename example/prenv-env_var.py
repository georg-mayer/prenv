import os

def read_envs() -> dict:
    """
    reads all gloable variables into a dict
    """
    env_dict: dict = dict()

    ##PRENV##env_dict['$VAR'] = os.getenv('$VAR')

    return env_dict