#!/usr/bin/env python3

"""
プロジェクトに必要な定数を定義する
"""

import os
from typing import List


def make_environ_fname(dirname: str) -> str:
    return os.path.join(dirname, "environ")

def check_environ(envfname: str) -> str:
    environ = "dev"
    try:
        if os.path.isfile(envfname):
            with open(envfname, "r") as handle:
                env = handle.read().strip().lower()
                if env in ["dev", "prod"]:
                    environ = env
    except:
        pass
    return environ


if __name__ != "__main__":

    PROJECT_ROOT: str = \
        os.path.dirname(os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../")))

    APPCACHE: str = os.path.join(PROJECT_ROOT, "appcache")
    LOGS_DIR: str = os.path.join(PROJECT_ROOT, "logs")
    STATIC_DIR: str = os.path.join(PROJECT_ROOT, "static")
    TEMPLATES_DIR: str = os.path.join(PROJECT_ROOT, "templates")

    envfname = make_environ_fname(PROJECT_ROOT)
    environ = check_environ(envfname)

    CONFIG_DIR: str = os.path.join(PROJECT_ROOT,
                                   "conf",
                                   environ,
                                   "batch/application")

    DIRECTORIES: List[str] = [
        PROJECT_ROOT,
        APPCACHE,
        LOGS_DIR,
        STATIC_DIR,
        TEMPLATES_DIR,
        CONFIG_DIR
    ]

