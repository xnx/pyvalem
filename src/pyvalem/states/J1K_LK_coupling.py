"""
The J1K_LK_Coupling class, representing an atomic term symbol under
the coupling conditions J1l -> K, J1L2 -> K or L, S1 -> K. These
are described in Martin et al. (sec. 11.8.4 and 11.8.5). NB there is
currently no check that the coupling quantum numbers given actually
make sense:

W. C. Martin, W. Wiese, A. Kramida, "Atomic Spectroscopy" in "Springer
Handbook of Atomic, Molecular and Optical Physics", G. W. F. Drake (ed.),
https://doi.org/10.1007/978-3-030-73893-8_11
"""

import pyparsing as pp

from pyvalem._utils import float_to_fraction, parse_fraction
from pyvalem.states._base_state import (
    State,
    StateParseError,
    StateValidationError,
)

integer = pp.Word(pp.nums)
Smult = integer.set_results_name("Smult")

fraction = integer + pp.Optional(pp.Suppress("/") + "2")
Kstr = fraction.set_results_name("Kstr")
Jstr = fraction.set_results_name("Jstr")
parity = pp.Literal("o").set_results_name("parity")

J1K_LK_term = (
    Smult
    + pp.Suppress("[")
    + Kstr
    + pp.Suppress("]")
    + pp.Optional(parity)
    + pp.Optional(pp.Suppress("_") + Jstr)
    + pp.StringEnd()
)


class J1K_LK_CouplingError(StateParseError):
    pass


class J1K_LK_CouplingValidationError(J1K_LK_CouplingError, StateValidationError):
    pass


class J1K_LK_Coupling(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.Smult = None
        self.K = None
        self.J = None
        self._parse_state(state_str)
        self._warn_deprecated_syntax(state_str)

    def _parse_state(self, state_str):
        try:
            components = J1K_LK_term.parse_string(state_str, parse_all=True)
        except pp.ParseException as err:
            raise J1K_LK_CouplingError(
                f'Invalid J1K / LK term symbol syntax:"{state_str}"'
            ) from err
        self.Smult = int(components.Smult)
        if self.Smult < 1:
            raise J1K_LK_CouplingValidationError(
                f"Invalid spin multiplicity in {state_str}"
            )
        self.S = (self.Smult - 1) / 2.0
        self.parity = components.get("parity")
        try:
            self.K = parse_fraction(components.Kstr)
        except ValueError as err:
            raise J1K_LK_CouplingError(err) from err
        try:
            self.J = parse_fraction(components.Jstr)
        except ValueError as err:
            raise J1K_LK_CouplingError(err) from err
        if self.J is not None:
            self._validate_J()

    def _validate_J(self):
        S_is_half_integer = int(2 * self.S) % 2
        K_is_half_integer = int(2 * self.K) % 2
        J_is_half_integer = int(2 * self.J) % 2
        if J_is_half_integer != S_is_half_integer ^ K_is_half_integer:
            raise J1K_LK_CouplingValidationError(
                f"J={self.J} is invalid for S={self.S}, K={self.K}."
            )
        if not abs(self.K - self.S) <= self.J <= self.K + self.S:
            raise J1K_LK_CouplingValidationError(
                f"Invalid J1K_LK coupling symbol: {self.state_str}"
                " |K-S| <= J <= K+S must be satisfied."
            )

    @property
    def html(self):
        parity_html = ""
        if self.parity:
            parity_html = "<sup>o</sup>"
        J_html = ""
        if self.J is not None:
            J_html = f"<sub>{float_to_fraction(self.J)}</sub>"
        html_chunks = [
            f"<sup>{str(self.Smult)}</sup>",
            f"[{float_to_fraction(self.K)}]",
            parity_html,
            J_html,
        ]
        return "".join(html_chunks)

    @property
    def latex(self):
        parity_latex = ""
        if self.parity:
            parity_latex = "^o"
        J_latex = ""
        if self.J is not None:
            J_latex = f"_{{{float_to_fraction(self.J)}}}"
        latex_chunks = [
            "{}" + f"^{{{self.Smult}}}",
            f"[{float_to_fraction(self.K)}]",
            parity_latex,
            J_latex,
        ]
        return "".join(latex_chunks)

    def __repr__(self):
        return self.state_str
