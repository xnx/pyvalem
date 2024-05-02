import unittest

from pyvalem import states


class StatesImportTest(unittest.TestCase):
    def test_state_types_import(self):
        self.assertIn("AtomicTermSymbol", states.__dict__)
        self.assertIn("CompoundLSCoupling", states.__dict__)
