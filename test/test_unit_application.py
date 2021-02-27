import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from typing import Any
import main_application as app


class TestApplication(unittest.TestCase):

    def __init__(self, *positional: Any, **keyword: Any) -> None:
        unittest.TestCase.__init__(self, *positional, **keyword)

    def test_0(self) -> None:
        application = app.Application()
        self.assertIsNotNone(application)
