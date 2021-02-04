import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

import main_dbapplication as app


class TestMainDBApplication(unittest.TestCase):

    def __init__(self, *positional, **keyword):
        unittest.TestCase.__init__(self, *positional, **keyword)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_0(self):
        application = app.DBApplication()
        self.assertIsNotNone(application)

    def test_1(self):
        application = app.DBApplication()
        self.assertIsNotNone(application)

        application.setup_resource()
        application.setup_application()

        ret = application.get_something_record()
        self.assertIsNotNone(ret)
