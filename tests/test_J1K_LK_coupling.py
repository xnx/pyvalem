"""
Unit tests for the J1K_LK_coupling module of PyValem.
"""

import unittest

from pyvalem.states.J1K_LK_coupling import (
    J1K_LK_Coupling,
    J1K_LK_CouplingError,
    J1K_LK_CouplingValidationError,
)


class J1K_LK_CouplingTest(unittest.TestCase):
    def test_J1K_LK_coupling(self):
        t0 = J1K_LK_Coupling("2[9/2]")
        self.assertEqual(t0.html, "<sup>2</sup>[9/2]")
        self.assertEqual(t0.latex, "{}^{2}[9/2]")

        t1 = J1K_LK_Coupling("2[9/2]_5")
        self.assertEqual(t1.html, "<sup>2</sup>[9/2]<sub>5</sub>")
        self.assertEqual(t1.latex, "{}^{2}[9/2]_{5}")

        t2 = J1K_LK_Coupling("3[9/2]o_11/2")
        self.assertEqual(t2.html, "<sup>3</sup>[9/2]<sup>o</sup><sub>11/2</sub>")
        self.assertEqual(t2.latex, "{}^{3}[9/2]^o_{11/2}")

    def test_J_validation(self):
        with self.assertRaises(J1K_LK_CouplingValidationError):
            J1K_LK_Coupling("2[9/2]_11/2")
        with self.assertRaises(J1K_LK_CouplingValidationError):
            J1K_LK_Coupling("3[9/2]o_5")
        with self.assertRaises(J1K_LK_CouplingValidationError):
            J1K_LK_Coupling("2[9/2]o_3")
