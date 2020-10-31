#!/usr/bin/env python3

"""
docstring is here
"""

import argparse

import common.framework.application.baseapplication as appframe
import common.data.dao as dao

global LOGGER


class Application(appframe.BaseApplication):

    def __init__(self):
        super().__init__(__name__, __file__)

    def validate_config(self):
        pass

    def setup_resource(self):
        pass

    def setup_application(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument("fname", type=str,
                               help="sample command line argument")

        self.args = argparser.parse_args()

    def run_application(self):
        print("hello, world")
        for each in self.get_cache_keys():
            print(each)
        print("fname: %s" % self.args.fname)

    def teardown_application(self):
        pass

    def teardown_resource(self):
        pass


if __name__ == "__main__":
    app = Application()
    LOGGER = app.create_toplevel_logger()
    app.start()
