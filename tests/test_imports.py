import unittest

from pyvalem import states
from pyvalem.states._state_parser import STATES


class StatesImportTest(unittest.TestCase):
    def test_state_types_import(self):
        self.assertIn("AtomicTermSymbol", states.__dict__)
        self.assertIn("CompoundLSCoupling", states.__dict__)


class StatesInitFileTest(unittest.TestCase):
    def test___init___imports(self):
        for StateClass in STATES.keys():
            self.assertIn(StateClass.__name__, states.__dict__)
