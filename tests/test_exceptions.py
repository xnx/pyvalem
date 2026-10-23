"""
Unit tests for the exceptions raised by PyValem.
"""

import unittest

from pyvalem import (
    Formula,
    FormulaParseError,
    PyValemError,
    Reaction,
    ReactionParseError,
    StatefulSpecies,
    StatefulSpeciesError,
    states,
)


class ExceptionHierarchyTest(unittest.TestCase):
    def test_common_base(self):
        for exc in (
            FormulaParseError,
            StatefulSpeciesError,
            ReactionParseError,
            states.StateError,
            states.StateParseError,
            states.RacahSymbolError,
            states.J1K_LK_CouplingValidationError,
            states.J1J2_CouplingValidationError,
        ):
            with self.subTest(exc.__name__):
                self.assertTrue(issubclass(exc, PyValemError))
                self.assertTrue(issubclass(exc, ValueError))

    def test_errors_raised(self):
        cases = (
            (Formula, "Xx"),
            (StatefulSpecies, "H2 v"),
            (StatefulSpecies, "H J=0 J=1"),
            (Reaction, "H -> He"),
            (states.RacahSymbol, "5p[3/2"),
            (states.GenericExcitedState, "*****"),
        )
        for cls, s in cases:
            with self.subTest(s):
                self.assertRaises(PyValemError, cls, s)
        self.assertRaises(states.RacahSymbolError, states.RacahSymbol, "5p[3/2")
        self.assertRaises(
            states.GenericExcitedStateError, states.GenericExcitedState, "*****"
        )

    def test_non_string_input(self):
        classes = (
            Formula,
            StatefulSpecies,
            Reaction,
            states.AtomicConfiguration,
            states.AtomicTermSymbol,
            states.KeyValuePair,
            states.VibrationalState,
        )
        for cls in classes:
            for value in (None, 3, ["H"]):
                with self.subTest(cls=cls.__name__, value=value):
                    self.assertRaises(TypeError, cls, value)


if __name__ == "__main__":
    unittest.main()
