import os

def read_envs() -> dict:
    """
    reads all gloable variables into a dict
    """
    env_dict: dict = dict()

    ##PRENV##env_dict['$VAR'] = os.getenv('$VAR')
    env_dict['PROJECTNAME'] = os.getenv('PROJECTNAME')
    env_dict['LOGLEVEL'] = os.getenv('LOGLEVEL')
    env_dict['BASEURL'] = os.getenv('BASEURL')
    env_dict['CONTEXT'] = os.getenv('CONTEXT')
    env_dict['LOCALBASEDIR'] = os.getenv('LOCALBASEDIR')

    return env_dict