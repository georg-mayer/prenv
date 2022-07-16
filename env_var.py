def read_envs() -> dict:
    """
    reads all gloable variables into a dict
    """
    env_dict: dict = dict()

    ##PRENV##env_dict['$VAR'] = "$VAL"
    env_dict['PROJECTNAME'] = "prenv_is_so_cooool"
    env_dict['LOGLEVEL'] = "INFO"
    env_dict['BASEURL'] = "127.0.0.1:8001"
    env_dict['CONTEXT'] = "./../../.."
    env_dict['LOCALBASEDIR'] = "${CONTEXT}/${PROJECTNAME}"

    return env_dict