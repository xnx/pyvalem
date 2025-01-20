"""
The J1J2_Coupling class, representing a complex atomic state with two
groups of separately spin-orbit coupled electrons giving rise to a
(J1, J2) term symbol, perhaps further coupled to a total (J1, J2)_J
level, with or without parity designator.

W. C. Martin, W. Wiese, A. Kramida, "Atomic Spectroscopy" in "Springer
Handbook of Atomic, Molecular and Optical Physics", G. W. F. Drake (ed.),
https://doi.org/10.1007/978-3-030-73893-8_11

Includes methods for parsing a string into quantum numbers and labels,
creating an HTML representation of the term symbol, etc.
"""

import pyparsing as pp

from pyvalem._utils import parse_fraction, float_to_fraction
from pyvalem.states._base_state import State, StateParseError

integer = pp.Word(pp.nums)
J1str = (integer + pp.Optional(pp.Suppress("/") + "2")).setResultsName("J1str")
J2str = (integer + pp.Optional(pp.Suppress("/") + "2")).setResultsName("J2str")
Jstr = (integer + pp.Optional(pp.Suppress("/") + "2")).setResultsName("Jstr")
parity = pp.Literal("o").setResultsName("parity")
J1J2_term = (
    "("
    + J1str
    + ","
    + J2str
    + ")"
    + pp.Optional(parity)
    + pp.Optional(pp.Suppress("_") + Jstr)
    + pp.StringEnd()
)


class J1J2_CouplingError(StateParseError):
    pass


class J1J2_CouplingValidationError(ValueError):
    pass


class J1J2_Coupling(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.J1 = None
        self.J2 = None
        self.parity = None
        self.J = None
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        try:
            components = J1J2_term.parseString(state_str)
        except pp.ParseException:
            raise J1J2_CouplingError(f"Invalid J1J2 coupling term syntax: {state_str}")
        self.J1 = parse_fraction(components.J1str)
        self.J2 = parse_fraction(components.J2str)
        self.J = parse_fraction(components.get("Jstr"))
        self.parity = components.get("parity")

        if self.J is not None:
            self._validate_J()

    def _validate_J(self):
        J1_is_half_integer = int(2 * self.J1) % 2
        J2_is_half_integer = int(2 * self.J2) % 2
        J_is_half_integer = int(2 * self.J) % 2
        if (J1_is_half_integer == J2_is_half_integer) == J_is_half_integer:
            raise J1J2_CouplingValidationError(
                f"J={self.J} is invalid for J1={self.J1} and J2={self.J2}."
            )
        if not abs(self.J1 - self.J2) <= self.J <= self.J1 + self.J2:
            raise J1J2_CouplingValidationError(
                f"Invalid atomic term symbol: {self.state_str}"
                f" |J1-J2| <= J <= J1+J2 must be satisfied."
            )

    @property
    def html(self):
        html_chunks = [f"({float_to_fraction(self.J1)}, {float_to_fraction(self.J2)})"]
        if self.parity:
            html_chunks.append("<sup>o</sup>")
        if self.J is not None:
            J_str = float_to_fraction(self.J)
            html_chunks.append(f"<sub>{J_str}</sub>")
        return "".join(html_chunks)

    @property
    def latex(self):
        latex_chunks = [f"({float_to_fraction(self.J1)}, {float_to_fraction(self.J2)})"]
        if self.parity:
            latex_chunks.append("^o")
        if self.J is not None:
            J_str = float_to_fraction(self.J)
            latex_chunks.append("_{{{}}}".format(J_str))
        return "".join(latex_chunks)

    def __repr__(self):
        return self.state_str
