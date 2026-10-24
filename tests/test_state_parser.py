"""
Unit tests for the parsing of state strings into the right type of state.
"""

import unittest

from pyvalem.stateful_species import StatefulSpecies, StatefulSpeciesError
from pyvalem.states import (
    AtomicConfigurationValidationError,
    AtomicTermSymbol,
    AtomicTermSymbolValidationError,
    CompoundLSCouplingValidationError,
    DiatomicMolecularConfigurationValidationError,
    J1J2_Coupling,
    J1J2_CouplingValidationError,
    J1K_LK_Coupling,
    J1K_LK_CouplingValidationError,
    KeyValuePair,
    MolecularTermSymbol,
    RacahSymbol,
    RotationalState,
    StateParseError,
    VibrationalState,
)
from pyvalem.states._state_parser import state_parser


class StateParserTest(unittest.TestCase):
    def test_invalid_states_are_reported(self):
        # These have the syntax of a type of state but describe a state that
        # can't exist: the reason is reported rather than "Could not parse".
        cases = {
            "2P_5/2": AtomicTermSymbolValidationError,
            "3P_3": AtomicTermSymbolValidationError,
            "1d": AtomicConfigurationValidationError,
            "1s3": AtomicConfigurationValidationError,
            "1s2.1s1": AtomicConfigurationValidationError,
            "1σ3": DiatomicMolecularConfigurationValidationError,
            "2[1/2]_7": J1K_LK_CouplingValidationError,
            "(1/2,1/2)_3": J1J2_CouplingValidationError,
            "2s2.2p(2Po_5/2)5g": CompoundLSCouplingValidationError,
        }
        for s, exc in cases.items():
            with self.subTest(s):
                self.assertRaises(exc, state_parser, s)

    def test_reserved_keys(self):
        # J=, v= and ν= states are never generic key-value pairs.
        for s in ("J=-1", "J=1/3", "J=0.25", "v=1.5", "v=1.5x", "ν=x"):
            with self.subTest(s):
                self.assertRaises(StateParseError, state_parser, s)
        self.assertIsInstance(state_parser("ν=1"), VibrationalState)
        self.assertEqual(repr(state_parser("ν=1")), "v=1")
        self.assertIsInstance(state_parser("J=1.0"), RotationalState)
        self.assertEqual(repr(state_parser("J=1.0")), "J=1")
        self.assertIsInstance(state_parser("n=1"), KeyValuePair)

    def test_one_rotational_state(self):
        # J=1.0 used to become a key-value pair, allowing a second J.
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "HCl J=2 J=1.0")

    def test_vibrational_states_written_with_v(self):
        # v is also an atomic orbital letter (l = 17).
        for s in ("2v1", "18v1", "20v3", "2v1+18v2"):
            with self.subTest(s):
                self.assertIsInstance(state_parser(s), VibrationalState)

    def test_whitespace(self):
        cases = (
            (AtomicTermSymbol, "2 P_1/2"),
            (AtomicTermSymbol, " 2P_1/2"),
            (MolecularTermSymbol, "X 1Σ+"),
            (MolecularTermSymbol, "X(1Σ+ )"),
            (RacahSymbol, "5p [3/2]_1"),
            (J1J2_Coupling, "(5/2, 1/2)_2"),
            (J1K_LK_Coupling, "2 [9/2]"),
        )
        for cls, s in cases:
            with self.subTest(s):
                self.assertRaises(StateParseError, cls, s)
                self.assertRaises(StateParseError, state_parser, s)

    def test_leading_zeros(self):
        for s in ("v=007", "J=01", "01*", "01s2", "1s02", "02P", "X(2Π_-03/2)"):
            with self.subTest(s):
                self.assertRaises(StateParseError, state_parser, s)

    def test_bare_number(self):
        self.assertRaises(StateParseError, state_parser, "2")
        self.assertRaises(StateParseError, StatefulSpecies, "CO 2")

    def test_zeros_that_are_valid(self):
        for s in ("v=0", "J=0", "J=10", "1S_0", "0v1+0v2", "3d10", "10*"):
            with self.subTest(s):
                state_parser(s)

    def test_unparseable_state(self):
        with self.assertRaisesRegex(StateParseError, "Could not parse"):
            state_parser("xyzzy")


if __name__ == "__main__":
    unittest.main()
