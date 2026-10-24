"""
The RotationalState class, representing a rotational quantum number, with
methods for parsing a string into a value and an HTML representation, etc.
"""

import pyparsing as pp

from pyvalem._grammar import uint
from pyvalem.states._base_state import State, StateParseError

integer = uint
integer_string = (integer + pp.StringEnd()).set_results_name("integer")
frac_string = (
    integer + pp.Suppress("/") + pp.Suppress(pp.Literal("2")) + pp.StringEnd()
).set_results_name("fraction_half")
decimal_string = (
    integer + pp.Suppress(".") + pp.Suppress(pp.Literal("5")) + pp.StringEnd()
).set_results_name("decimal_half")
decimal_integer_string = (
    integer + pp.Suppress(".") + pp.Suppress(pp.Literal("0")) + pp.StringEnd()
).set_results_name("decimal_integer")

Jstr = (
    integer_string | frac_string | decimal_string | decimal_integer_string
).leave_whitespace()


class RotationalStateError(StateParseError):
    pass


class RotationalState(State):
    def __init__(self, state_str):
        self.state_str = None
        self.J = None
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        try:
            k, v = state_str.split("=")
            if k != "J":
                raise ValueError
        except ValueError:
            raise RotationalStateError(
                'Rotational states must start with "J="'
            ) from None

        state_str = v

        self.J = None
        if state_str not in ("*", "**", "***"):
            try:
                components = Jstr.parse_string(state_str, parse_all=True)
            except pp.ParseException as err:
                raise RotationalStateError(
                    "Invalid rotational state value syntax: {0}".format(state_str)
                ) from err

            if "integer" in components:
                self.J = int(components["integer"][0])
            elif "fraction_half" in components:
                self.J = int(components["fraction_half"][0]) / 2
            elif "decimal_half" in components:
                self.J = float(components["decimal_half"][0]) + 0.5
                state_str = "{}/2".format(int(2 * self.J))
            elif "decimal_integer" in components:
                self.J = int(components["decimal_integer"][0])
                state_str = str(self.J)
            else:
                raise RotationalStateError(
                    "Invalid rotational state value syntax: {0}".format(state_str)
                )

            if self.J is not None:
                self._validate_j()

        self.state_str = "J={}".format(state_str)

    def _validate_j(self):
        if self.J % 0.5 != 0:
            raise RotationalStateError(
                "Invalid rotational state value: {}.Must be a multiple of 1/2.".format(
                    self.state_str
                )
            )

    def __repr__(self):
        return self.state_str
