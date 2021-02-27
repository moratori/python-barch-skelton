import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import main_dbapplication as app
from typing import Any


class TestMainDBApplication(unittest.TestCase):

    def __init__(self, *positional: Any, **keyword: Any) -> None:
        unittest.TestCase.__init__(self, *positional, **keyword)

    def test_0(self) -> None:
        application = app.DBApplication()
        self.assertIsNotNone(application)

    def test_1(self) -> None:
        application = app.DBApplication()
        self.assertIsNotNone(application)

        application.setup_resource()
        application.setup_application()

        ret = application.get_something_record()
        self.assertIsNotNone(ret)
