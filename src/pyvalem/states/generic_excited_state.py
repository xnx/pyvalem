"""
The GenericExcitedState class, representing an unspecified excited state of
an atom, ion or molecule as '*', '**', '***', '****', '5*', etc.
"""

import pyparsing as pp

from pyvalem.states._base_state import State, StateParseError

integer = pp.Word(pp.nums)
atom_int = integer.setResultsName("int")
state_term = (atom_int + "*" + pp.StringEnd()).leaveWhitespace()


class GenericExcitedStateError(StateParseError):
    pass


class GenericExcitedState(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.int_n = None
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        if "*" in state_str:
            if state_str.count("*") == len(state_str):
                if len(state_str) > 4:
                    raise StateParseError(
                        "Invalid excited state value: {0}"
                        " Can be *, **, ***, or ****".format(state_str)
                    )
            else:
                try:
                    components = state_term.parseString(state_str)
                    self.int_n = int(components.int)
                except pp.ParseException:
                    raise GenericExcitedStateError(
                        "Invalid excited state value syntax: {0} has to be of form"
                        " n* with n = integer".format(state_str)
                    )
        else:
            raise GenericExcitedStateError(
                "Invalid excited state value"
                " syntax: {0} Must have a * term.".format(state_str)
            )

    def __repr__(self):
        if self.state_str == "1*":
            return "*"
        elif self.state_str == "2*":
            return "**"
        elif self.state_str == "***":
            return "3*"
        elif self.state_str == "****":
            return "4*"
        return self.state_str

    @property
    def html(self):
        return "<sup>{:s}</sup>".format(repr(self))

    @property
    def latex(self):
        return "^{{{:s}}}".format(repr(self))
