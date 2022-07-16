# prenv v0.1

Environment variables preprocessor e.g. for docker-compose, docker, python and php. 

> _Keep your `.env` file the single source of environment variable defintion!_

> prenv keeps your coding projects variable names and values aligned over any kind of programming langugae or configuration file. 

> prenv solves the "no includes" problem for docker/docker-compose files


&nbsp;  
# Background

DockerFiles and docker-compose files currently don't allow include statements. Bigger projects end up in large numbers of environment variables which all need to be kept in-sync over many different files, which cause massive waste of time when e.g. a newly introduced environment variable was forgotten to be added to a pythong modul. 

Prenv resolvs these issues by reading all variables from the local .env file and put them into any type and number of files based on a _user-defined template_. The whole mechanism is very simple but effective.

This works not only for docker, but also in any programming language that accepts either `##` or `//` as single line comments.

&nbsp;  
# Functionality So Far

- reads all variables and their values from the .env file in the local directory

- finds all files in the local directory which have the tag `prenv-` in the filename
- in any of these files include tags of the form 
    - `##PRENV##<template>` (e.g. for docker, docker-compose, python); or 
    - `//PRENV//<template>` (e.g. for php)

    and prenv will:

    1) add below the template for each environment variable add a new line, based on the template:

    2) use the same indent as the template used;

    3) will replace any occurence of `$VAR` in the template with the name of the environment variable;

    4) will replace any occurence of `${VAR}` with `${NAME_OF_ENVIRONMET_VAR}`;

    6) will replace any occurence of `$VAL` with the value of the environment variable;

    6) will store the changes in a new file (in the same directory) with the same name as the original file, only with the tage `prenv-` removed from the filename.

&nbsp;   
# Example

This is the example `.env` file:
```
PROJECTNAME=prenv_is_so_cooool
LOGLEVEL=INFO
BASEURL=127.0.0.1:8001
CONTEXT=./../../..
LOCALBASEDIR=${CONTEXT}/${PROJECTNAME}
```

The `prenv-test.yml` file looks like this:
```
variables:
    ##PRENV##- $VAR=$VAL

project:
    args:
        //PRENV//- $VAR=${VAR}
```

After running prenv with `/usr/bin/python3 prenv.py` a new `test.yml` file is created with the following content:
```
variables:
    ##PRENV##- $VAR=$VAL
    - PROJECTNAME=prenv_is_so_cooool
    - LOGLEVEL=INFO
    - BASEURL=127.0.0.1:8001
    - CONTEXT=./../../..
    - LOCALBASEDIR=${CONTEXT}/${PROJECTNAME}

project:
    args:
        //PRENV//ENV $VAR=${VAR}
        ENV PROJECTNAME=${PROJECTNAME}
        ENV LOGLEVEL=${LOGLEVEL}
        ENV BASEURL=${BASEURL}
        ENV CONTEXT=${CONTEXT}
        ENV LOCALBASEDIR=${LOCALBASEDIR}
```
Note that you can re-use the same variable names in e.g. python to read all these variables e.g. into a dictionary. So the `prenv-env_var.py` file:
```
def read_envs() -> dict:
    """
    reads all gloable variables into a dict
    """
    env_dict: dict = dict()

    ##PRENV##env_dict['$VAR'] = "$VAL"
    
    return env_dict
```

after running prenv becomes the `env_var.py` file:
```
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
```

&nbsp;  
# Planned for upcoming versions
- should work also with python - needs testing;
- needs additional comment tags to work also with php;
- include an additional tag which allows to change a specifc variable at a specific location, e.g. `name: ###PRENV###$_PROJECTNAME###` should result in `name: prenv_is_so_cooool` in the above example;
- allow different input and output directories;
- regulate verbosity with a -v CLI flag;
- add a restriction tag in variable names, which will then only applied when converting specific files, skipped for others, e.g. the `.env` variable names could be trailed by something like "`SEC_`". 


&nbsp;  
# Limitations
- only works on files in a single directory;
- variables cannot be skipped, i.e. it is not possible to have only a subset of variables put into a file.
