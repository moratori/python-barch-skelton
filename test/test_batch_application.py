import unittest
import srcpath  # noqa
from typing import Any

import batch_application as app


class TestApplication(unittest.TestCase):

    def __init__(self, *positional: Any, **keyword: Any) -> None:
        unittest.TestCase.__init__(self, *positional, **keyword)

    def test_0(self) -> None:
        application = app.Application()
        self.assertIsNotNone(application)
