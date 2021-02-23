#!/usr/bin/env python3

"""
docstring is here
"""

import argparse
from typing import Any
import common.framework.application.baseapplication as appframe

global LOGGER


class Application(appframe.BaseApplication):

    def __init__(self) -> None:
        super().__init__(__name__, __file__)

    def validate_config(self) -> None:
        pass

    def setup_resource(self) -> None:
        pass

    def setup_application(self) -> None:
        argparser = argparse.ArgumentParser()
        argparser.add_argument("fname", type=str,
                               help="sample command line argument")

        self.args = argparser.parse_args()

    def run_application(self, **args: Any) -> None:
        print("hello, world")
        for each in self.get_cache_keys():
            print(each)
        print("fname: %s" % self.args.fname)

    def teardown_application(self) -> None:
        pass

    def teardown_resource(self) -> None:
        pass


if __name__ == "__main__":
    app = Application()
    LOGGER = app.create_toplevel_logger()
    app.start()
