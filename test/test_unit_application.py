import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import main_application as app


class TestApplication(unittest.TestCase):

    def __init__(self, *positional, **keyword):
        unittest.TestCase.__init__(self, *positional, **keyword)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_0(self):
        application = app.Application()
        self.assertIsNotNone(application)
