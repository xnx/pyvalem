"""
The RotationalState class, representing a rotational quantum number, with
methods for parsing a string into a value and an HTML representation, etc.
"""

import pyparsing as pp

from .state import State, StateParseError

integer = pp.Word(pp.nums)
integer_string = (integer + pp.StringEnd()).setResultsName("integer")
frac_string = (
    integer + pp.Suppress("/") + pp.Suppress(pp.Literal("2")) + pp.StringEnd()
).setResultsName("fraction_half")
decimal_string = (
    integer + pp.Suppress(".") + pp.Suppress(pp.Literal("5")) + pp.StringEnd()
).setResultsName("decimal_half")

Jstr = integer_string | frac_string | decimal_string


class RotationalStateError(StateParseError):
    pass


class RotationalState(State):
    def __init__(self, state_str):
        self.state_str = None
        self.J = None
        self.parse_state(state_str)

    def parse_state(self, state_str):

        try:
            k, v = state_str.split("=")
            if k.strip() != "J":
                raise ValueError
        except ValueError:
            raise RotationalStateError("Rotational states must start with" ' "J="')

        state_str = v.strip()

        self.J = None
        if state_str not in ("*", "**", "***"):
            try:
                components = Jstr.parseString(state_str)
            except pp.ParseException:
                raise RotationalStateError(
                    "Invalid rotational state value" " syntax: {0}".format(state_str)
                )

            if "integer" in components:
                self.J = int(components["integer"][0])
            elif "fraction_half" in components:
                self.J = int(components["fraction_half"][0]) / 2
            elif "decimal_half" in components:
                self.J = float(components["decimal_half"][0]) + 0.5
                state_str = "{}/2".format(int(2 * self.J))
            else:
                raise RotationalStateError(
                    "Invalid rotational state value" " syntax: {0}".format(state_str)
                )

            if self.J is not None:
                self.validate_j()

        self.state_str = "J={}".format(state_str)

    def validate_j(self):
        if self.J % 0.5 != 0:
            raise RotationalStateError(
                "Invalid rotational state value: {}."
                "Must be a multiple of 1/2.".format(self.state_str)
            )
