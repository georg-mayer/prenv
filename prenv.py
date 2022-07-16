#!/usr/bin/python3
"""
Replace environment variable settings in docker-compose.yaml and *.Dockerfile with data provided in .env files
"""

import typing
import logging
import inspect
import os
import re 

g_fname_env: str = '.env'
g_fname_template_string: str = 'prenv-'

# note: trigger strings must all have the same length
g_trigger_strings: list[str] = [
    '##PRENV##',
    '//PRENV//'
    ]
g_len_trigger_string = len(g_trigger_strings[0])

g_logger_name = 'prenv'
g_loglevel = 'DEBUG'


def func_name(i: int = 0) -> str:
    """
    returns the name of the calling function
    """
    return inspect.stack()[1+i].function

def set_logger(
    logger_name: str,
    log_level: str = 'WARNING'
    ) -> logging.Logger:
    """
    creates or resets the local logger with the desired log_level
    """
    logging.basicConfig()
    logger: logging.Logger = logging.getLogger(logger_name)
    while logger.hasHandlers() and len(logger.handlers) > 0:
        logger.removeHandler(logger.handlers[0])
    loglevel = logging.getLevelName(log_level)
    logger.setLevel(loglevel)
    return logger

def open_file(
    fname: str,
    mode: str
    ) -> typing.TextIO:
    """
    opens a textfile in the given mode, handles exceptions and catches/reports related errors
    """
    logger: logging.Logger = logging.getLogger(g_logger_name)

    try:
        f: typing.TextIO = open(fname,mode)
    except Exception as e:
        logger.error(f'{func_name(1)}: file {fname} could not be read:\n{e}')
        return None
    return f

def write_file(
    f: typing.TextIO
    ) -> None:
    """
    writes a textfile in the given mode, handles exceptions and catches/reports related errors
    """
    logger: logging.Logger = logging.getLogger(g_logger_name)

    try: 
        f.close()
    except Exception as e:
        logger.error(f'{func_name(1)}: file {f.name} could not be written:\n{e}')
    return None


def read_env(fname: str = g_fname_env) -> dict():
    """
    reads all environment variable names and their defintion from .env
    """
    logger: logging.Logger = logging.getLogger(g_logger_name)
    env_vars: dict = dict()

    env: typing.TextIO = open_file(fname,'r')
    if env == None:
        return None
    lines = env.readlines()
    env.close()
    lines_all: int = len(lines) - 1

    lc: int = 0
    while lc <= lines_all:
        line: str = lines[lc].strip()
        if len(line) > 0 and "=" in line:
            key_match  = re.findall('^([^=]*)=.*',line)
            value_match = re.findall('^[^=]*=[ ]*(.*)',line)
            if key_match and value_match:
                env_vars[key_match[0]] = value_match[0]
        lc += 1
    
    return env_vars

def convert_template_file(
    env_vars: dict(),
    fname_in: str,
    fname_out: str
    ) -> None:
    """
    adds behind all template-trigger-lines in a template file the related environment-variable lines and writes them to a new file
    takes the form of 
    - ${ENVNAME}=${ENVNAME}
    """
    logger: logging.Logger = logging.getLogger(g_logger_name)

    new_lines: list[str] = []
    fin: typing.TextIO = open_file(fname_in,'r')
    lines = fin.readlines()
    fin.close()
    lines_all: int = len(lines) - 1

    lc: int = 0
    while lc <= lines_all:
        line: str = lines[lc]
        lc += 1
        line_start = line.strip()[:g_len_trigger_string]
        if len(line) > 0 and  line_start in g_trigger_strings:
            trigger_string = line_start
            new_lines.append(line)
            new_line_template: str = line.replace(trigger_string,'')
            for k,v in env_vars.items():
                new_line = new_line_template.replace('$VAR',k).replace('${VAR}', '${' + k + '}').replace('$VAL', v)
                new_lines.append(new_line)
        else:
            new_lines.append(line)

    fout: typing.TextIO = open_file(fname_out,'w')
    fout.writelines(new_lines)
    write_file(fout)


def main() -> None:
    """
    main function
    runs through all prenv-files in the local directory
    """

    logger = set_logger(g_logger_name,g_loglevel)

    envs: dict = read_env()
    if envs:
        for file_name in os.listdir():
            if g_fname_template_string in file_name:
                new_file_name = file_name.replace(g_fname_template_string,'')
                print(f'{file_name} ==> {new_file_name}')
                convert_template_file(
                    envs,
                    file_name,
                    new_file_name
                )
    
if __name__ == '__main__':
    main()