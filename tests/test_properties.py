"""
Property-based tests: whatever the string, PyValem either parses it or raises
one of its own exceptions, and what it parses can be parsed again from its
canonical representation.
"""

import unittest

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from pyvalem import Formula, PyValemError, Reaction, StatefulSpecies
from pyvalem.states._state_parser import STATES, state_parser

# Mostly characters used in formulas, states and reactions, so that the strings
# get further into the parsers than random text would.
ALPHABET = "HCNOSPDTMBFKLIRZexvνJnlspdfgσπδΣΠΔΦΓuo0123456789+-()[]{}.,;=*/_'\"· →⇌<>"
strings = st.text(alphabet=ALPHABET, max_size=24) | st.text(max_size=12)

settings.register_profile(
    "pyvalem", deadline=None, suppress_health_check=[HealthCheck.too_slow]
)
settings.load_profile("pyvalem")


def parse(cls, s, **kwargs):
    """Return cls(s), or None if PyValem rejects s."""
    try:
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
    def test_states(self, s):
        for StateClass in STATES:
            state = parse(StateClass, s)
            if state is not None:
                self.assertEqual(StateClass(repr(state)), state)

    @given(strings)
    def test_stateful_species(self, s):
        species = parse(StatefulSpecies, s)
        if species is not None:
            self.assertEqual(StatefulSpecies(repr(species)), species)

    @given(strings)
    def test_reaction(self, s):
        reaction = parse(Reaction, s, strict=False)
        if reaction is not None:
            self.assertEqual(Reaction(str(reaction), strict=False), reaction)


if __name__ == "__main__":
    unittest.main()
