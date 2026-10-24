"""
The VibrationalState class, representing a molecular vibrational state, with
methods for parsing a string into quantum numbers and labels, creating
an HTML representation of it, etc.
"""

import pyparsing as pp

from pyvalem._grammar import uint
from pyvalem.states._base_state import (
    State,
    StateParseError,
    StateValidationError,
)

integer = uint

# noinspection PyTypeChecker
vibrational_term = pp.Group(
    pp.Optional(integer.set_results_name("n"), default=1)
    + pp.Or(("v", "ν"))
    + integer.set_results_name("mode")
)
vibrational_config = (
    vibrational_term
    + pp.ZeroOrMore(pp.Suppress("+") + vibrational_term)
    + pp.StringEnd()
).leave_whitespace()


class VibrationalTerm:
    def __init__(self, n, mode):
        self.n = int(n)
        self.mode = int(mode)

    def __repr__(self):
        return "{}ν{:d}".format(self.n if self.n != 1 else "", self.mode)

    @property
    def html(self):
        return "{}ν<sub>{:d}</sub>".format(self.n if self.n != 1 else "", self.mode)

    @property
    def latex(self):
        return "{}\\nu_{{{:d}}}".format(self.n if self.n != 1 else "", self.mode)

    def __lt__(self, other):
        return self.mode < other.mode


class VibrationalStateError(StateParseError):
    pass


class VibrationalStateValidationError(VibrationalStateError, StateValidationError):
    pass


class VibrationalState(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.v = None
        self.polyatomic = None
        self.terms = None
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        self.polyatomic = False

        def get_v(s_v):
            """Return the vibrational quantum number s_v, or None if it isn't one."""
            if s_v in ("*", "**", "***"):
                self.polyatomic = None
                return s_v
            # NB int() would also accept a sign, underscores and other digits.
            if s_v.isascii() and s_v.isdigit() and (s_v == "0" or s_v[0] != "0"):
                return int(s_v)
            return None

        if state_str.startswith(("v=", "ν=")):
            self.v = get_v(state_str[2:])
            if self.v is None:
                raise VibrationalStateError(
                    "Invalid vibrational state syntax: {}".format(state_str)
                )
            return

        self.v = get_v(state_str)
        if isinstance(self.v, int):
            raise VibrationalStateError(
                "A vibrational state must be written v={}, not {}".format(
                    self.v, state_str
                )
            )
        if self.v is not None:
            # An unspecified excitation: *, ** or ***.
            self.state_str = "v={}".format(state_str)
            return

        self.polyatomic = True
        try:
            parse_results = vibrational_config.parse_string(state_str, parse_all=True)
        except pp.ParseException as err:
            raise VibrationalStateError(
                "Invalid vibrational state configuration syntax: {0}".format(state_str)
            ) from err

        self.terms = [
            VibrationalTerm(parsed_term["n"], parsed_term["mode"])
            for parsed_term in parse_results
        ]
        self.terms.sort()
        modes = [term.mode for term in self.terms]
        if len(modes) != len(set(modes)):
            raise VibrationalStateValidationError(
                "Repeated vibrational mode in {}".format(state_str)
            )

    def __repr__(self):
        if self.v is not None:
            return "v={}".format(self.v)
        return "+".join([str(term) for term in self.terms])

    @property
    def html(self):
        if self.polyatomic:
            return " + ".join([term.html for term in self.terms])
        return str(self)

    @property
    def latex(self):
        if self.polyatomic:
            return " + ".join([term.latex for term in self.terms])
        return str(self)
