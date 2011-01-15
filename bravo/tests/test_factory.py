import shutil
import tempfile
import unittest

import bravo.config
import bravo.factory

class TestBetaFactory(unittest.TestCase):

    def setUp(self):
        # Same setup as World, because Factory is very automagical.
        self.d = tempfile.mkdtemp()
        self.name = "unittest"

        bravo.config.configuration.add_section("world unittest")
        bravo.config.configuration.set("world unittest", "world", self.d)
        bravo.config.configuration.set("world unittest", "port", "0")

        self.f = bravo.factory.BetaFactory(self.name)

    def tearDown(self):
        del self.f
        shutil.rmtree(self.d)

        bravo.config.configuration.remove_section("world unittest")

    def test_trivial(self):
        pass
