"""
Unit tests for the warnings about input that PyValem 3.0 will reject.
"""

import unittest
import warnings

from pyvalem import PyValemDeprecationWarning, Reaction, StatefulSpecies
from pyvalem.states import (
    AtomicTermSymbol,
    J1J2_Coupling,
    J1K_LK_Coupling,
    MolecularTermSymbol,
    RacahSymbol,
    RotationalState,
    VibrationalState,
)
from pyvalem.states._state_parser import state_parser


class StateDeprecationTest(unittest.TestCase):
    def test_bare_number(self):
        with self.assertWarnsRegex(PyValemDeprecationWarning, "write v=2"):
            VibrationalState("2")
        with self.assertWarnsRegex(PyValemDeprecationWarning, "write v=2"):
            StatefulSpecies("CO 2")

    def test_whitespace(self):
        cases = (
            (AtomicTermSymbol, "2 P_1/2"),
            (MolecularTermSymbol, "X 1Σ+"),
            (RotationalState, "J = 2"),
            (VibrationalState, "v = 2"),
            (RacahSymbol, "5p [3/2]_1"),
            (J1J2_Coupling, "(5/2, 1/2)_2"),
            (J1K_LK_Coupling, "2 [9/2]"),
        )
        for cls, s in cases:
            with (
                self.subTest(s),
                self.assertWarnsRegex(PyValemDeprecationWarning, "Whitespace"),
            ):
                cls(s)

    def test_leading_zeros(self):
        for s in ("v=007", "J=01", "01*", "01s2", "02P", "X(2Π_-03/2)"):
            with (
                self.subTest(s),
                self.assertWarnsRegex(PyValemDeprecationWarning, "Leading zeros"),
            ):
                state_parser(s)

    def test_valid_states_dont_warn(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            for s in (
                "v=0",
                "J=0",
                "J=10",
                "1S_0",
                "0v1+0v2",
                "3d10",
                "[Ar].3d10.4s2",
                "2P_1/2",
                "(5/2,1/2)_2",
                "10*",
            ):
                state_parser(s)


class ReactionDeprecationTest(unittest.TestCase):
    def test_leading_zeros_in_a_coefficient(self):
        with self.assertWarnsRegex(PyValemDeprecationWarning, "coefficient"):
            Reaction("02H -> H2")


class WarningLocationTest(unittest.TestCase):
    def test_warning_is_attributed_to_the_caller(self):
        with self.assertWarns(PyValemDeprecationWarning) as cm:
            StatefulSpecies("CO 2")
        self.assertEqual(cm.filename, __file__)


if __name__ == "__main__":
    unittest.main()
