import unittest

import pyvalem
from pyvalem import states
from pyvalem.states._state_parser import STATES


class StatesImportTest(unittest.TestCase):
    def test_state_types_import(self):
        self.assertIn("AtomicTermSymbol", states.__dict__)
        self.assertIn("CompoundLSCoupling", states.__dict__)


class StatesInitFileTest(unittest.TestCase):
    def test___init___imports(self):
        for StateClass in STATES:
            self.assertIn(StateClass.__name__, states.__dict__)
            self.assertIn(StateClass.__name__, states.__all__)


class PackageImportTest(unittest.TestCase):
    def test_top_level_names(self):
        for name in pyvalem.__all__:
            self.assertTrue(hasattr(pyvalem, name), name)
        self.assertIs(pyvalem.Formula, pyvalem.formula.Formula)

    def test_version(self):
        self.assertRegex(pyvalem.__version__, r"^\d+\.\d+\.\d+")
