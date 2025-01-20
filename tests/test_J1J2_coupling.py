"""
Unit tests for the J1J2_coupling module of PyValem.
"""

import unittest

from pyvalem.states.J1J2_coupling import (
    J1J2_Coupling,
    J1J2_CouplingError,
    J1J2_CouplingValidationError,
)


class J1J2_CouplingTest(unittest.TestCase):
    def test_J1J2_coupling(self):
        t0 = J1J2_Coupling("(1,3)")
        self.assertEqual(t0.J1, 1)
        self.assertEqual(t0.J2, 3)
        self.assertIsNone(t0.J)

        t1 = J1J2_Coupling("(2,3/2)o_1/2")
        self.assertEqual(t1.J1, 2)
        self.assertEqual(t1.J2, 1.5)
        self.assertEqual(t1.J, 0.5)

    def test_J_validation(self):
        with self.assertRaises(J1J2_CouplingValidationError):
            J1J2_Coupling("(1,1/2)_2")
        with self.assertRaises(J1J2_CouplingValidationError):
            J1J2_Coupling("(5/2,1/2)_1")
