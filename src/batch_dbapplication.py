#!/usr/bin/env python3

"""
docstring is here
"""

from typing import List

import common.framework.application.dbapplication.mysqlapplication as fw
from common.data.db.Something import Something
from common.framework.dbsession import local_session

global LOGGER


class DBApplication(fw.MySQLApplication):

    def __init__(self) -> None:
        super().__init__(__name__, __file__)

    def validate_config(self) -> None:
        super().validate_config()

    def setup_resource(self) -> None:
        super().setup_resource()

    def get_something_record(self) -> List[Something]:
        with local_session(self.thread_local_session_maker) as session:
            ret = session.query(Something).all()
        return ret

    def run_application(self) -> None:
        print("hello, world")
        for each in self.get_something_record():
            print("id: %s" % each.some_id)
            print("val: %s" % each.some_value)

    def teardown_resource(self) -> None:
        super().teardown_resource()


if __name__ == "__main__":
    dbapp = DBApplication()
    LOGGER = dbapp.create_toplevel_logger()
    dbapp.start()
