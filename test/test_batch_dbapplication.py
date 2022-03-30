import unittest
import srcpath  # noqa
from typing import Any

import batch_dbapplication as app


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
