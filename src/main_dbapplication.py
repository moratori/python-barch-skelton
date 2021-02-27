#!/usr/bin/env python3

"""
docstring is here
"""

from typing import Any, List
import common.framework.application.dbapplication.mysqlapplication as appframe
from common.data.table import Something
from common.framework.dbsession import local_session

global LOGGER


class DBApplication(appframe.MySQLApplication):

    def __init__(self) -> None:
        super().__init__(__name__, __file__)

    def validate_config(self) -> None:
        super().validate_config()

    def setup_resource(self) -> None:
        super().setup_resource()

    def get_something_record(self) -> List[Any]:
        with local_session(self.thread_local_session_maker) as session:
            ret = session.query(Something).all()
        with local_session(self.thread_local_session_maker) as session:
            ret = session.query(Something).all()
        return ret

    def setup_application(self) -> None:
        pass

    def run_application(self, **args: Any) -> None:
        print("hello, world")
        print(self.get_something_record())

    def teardown_application(self) -> None:
        pass

    def teardown_resource(self) -> None:
        pass


if __name__ == "__main__":
    dbapp = DBApplication()
    LOGGER = dbapp.create_toplevel_logger()
    dbapp.start()
