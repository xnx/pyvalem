"""
Property-based tests: whatever the string, PyValem either parses it or raises
one of its own exceptions, and what it parses can be parsed again from its
canonical representation.
"""

import unittest
import warnings

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from pyvalem import (
    Formula,
    PyValemDeprecationWarning,
    PyValemError,
    Reaction,
    StatefulSpecies,
)
from pyvalem.states._state_parser import STATES, state_parser

# Mostly characters used in formulas, states and reactions, so that the strings
# get further into the parsers than random text would.
ALPHABET = "HCNOSPDTMBFKLIRZexvνJnlspdfgσπδΣΠΔΦΓuo0123456789+-()[]{}.,;=*/_'\"· →⇌<>"
# Fragments of valid notation, which strings made from them reach further still.
TOKENS = (
    "H", "C", "O", "Cl", "D", "(13C)", "2", "3", "x", "+", "-", "(", ")", ".", "·",
    "1s2", "2p", "3d10", "[Ne]", "[Ar]", "2P", "_1/2", "o", "X", "1Σ+", "g", "u",
    "v=", "J=", "ν", "v", "1", "*", "[", "]", "3/2", "5p", "s'", "σ", "π", "sigma",
    " ", ";", ", ", "n=", " + ", " -> ", "e-", "hv", "M", "trans-", "1,2-", "(±)-",
    "{2}", "a", "z", "EF", "X\u0303",
)  # fmt: skip
strings = (
    st.text(alphabet=ALPHABET, max_size=24)
    | st.text(max_size=12)
    | st.lists(st.sampled_from(TOKENS), max_size=8).map("".join)
)

settings.register_profile(
    "pyvalem",
    max_examples=500,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
settings.load_profile("pyvalem")


def parse(cls, s, **kwargs):
    """Return cls(s), or None if PyValem rejects s."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", PyValemDeprecationWarning)
            return cls(s, **kwargs)
    except PyValemError:
        return None


class NoUnexpectedExceptionsTest(unittest.TestCase):
    @given(strings)
    def test_formula(self, s):
        parse(Formula, s)

    @given(strings)
    def test_states(self, s):
        for StateClass in STATES:
            parse(StateClass, s)
        parse(state_parser, s)

    @given(strings)
    def test_stateful_species(self, s):
        parse(StatefulSpecies, s)

    @given(strings)
    def test_reaction(self, s):
        parse(Reaction, s)
        parse(Reaction, s, strict=False)


class RoundTripTest(unittest.TestCase):
    @given(strings)
    def test_formula(self, s):
        formula = parse(Formula, s)
        if formula is not None:
            again = parse(Formula, repr(formula))
            self.assertEqual(again, formula)
            self.assertEqual(repr(again), repr(formula))

    @given(strings)
    def test_states(self, s):
        for StateClass in STATES:
            state = parse(StateClass, s)
            if state is not None:
                self.assertEqual(parse(StateClass, repr(state)), state)

    @given(strings)
    def test_stateful_species(self, s):
        species = parse(StatefulSpecies, s)
        if species is not None:
            self.assertEqual(parse(StatefulSpecies, repr(species)), species)

    @given(strings)
    def test_reaction(self, s):
        reaction = parse(Reaction, s, strict=False)
        if reaction is not None:
            self.assertEqual(parse(Reaction, str(reaction), strict=False), reaction)


if __name__ == "__main__":
    unittest.main()
