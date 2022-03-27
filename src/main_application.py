#!/usr/bin/env python3

"""
docstring is here
"""

import argparse

import common.framework.application.batchbaseapplication as fw

global LOGGER


class Application(fw.BatchBaseApplication):

    def __init__(self) -> None:
        super().__init__(__name__, __file__)

    def setup_application(self) -> None:
        argparser = argparse.ArgumentParser()
        argparser.add_argument("fname", type=str,
                               help="sample command line argument")

        self.args = argparser.parse_args()

    def run_application(self) -> None:
        print("hello, world")
        for each in self.get_cache_keys():
            print(each)
        print("fname: %s" % self.args.fname)


if __name__ == "__main__":
    app = Application()
    LOGGER = app.create_toplevel_logger()
    app.start()
