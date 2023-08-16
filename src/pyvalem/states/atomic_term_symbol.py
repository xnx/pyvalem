"""
The AtomicTermSymbol class, representing an atomic term symbol, with
methods for parsing a string into quantum numbers and labels, creating
an HTML representation of the term symbol, etc.
"""

import pyparsing as pp

from pyvalem.states._base_state import State, StateParseError
from pyvalem._utils import parse_fraction, float_to_fraction

atom_L_symbols = "S P D F G H I K L M N O Q R T U V W X Y Z".split()

integer = pp.Word(pp.nums)

# The single, lowercase letter label given in the Multiplet Table of C. E. Moore
# NBS Circ, No. 488 (1950) and sometimes used to distinguish terms with the same
# S, L from the same configuration. See e.g. G. Nave et al., Astrophys. J. Suppl. Ser.
# 94:221-459 (1994).
moore_label = pp.Char("abcdefghijklmnopqrstuvwxyz").setResultsName("moore_label")
atom_Smult = integer.setResultsName("Smult")
atom_Lletter = pp.oneOf(atom_L_symbols).setResultsName("Lletter")
atom_Jstr = (
    integer + pp.Optional(pp.Suppress("/") + "2") + pp.StringEnd()
).setResultsName("Jstr")
atom_parity = pp.Literal("o").setResultsName("parity")
atom_term = (
    pp.Optional(moore_label)
    + atom_Smult
    + atom_Lletter
    + pp.Optional(atom_parity)
    + pp.Optional(pp.Suppress("_") + atom_Jstr)
    + pp.StringEnd()
)


class AtomicTermSymbolError(StateParseError):
    pass


class AtomicTermSymbol(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.Smult = None
        self.S = None
        self.Lletter = None
        self.L = None
        self.parity = None
        self.J = None
        self.moore_label = ""
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        try:
            components = atom_term.parseString(state_str)
        except pp.ParseException:
            raise AtomicTermSymbolError(
                "Invalid atomic term symbol syntax:" " {0}".format(state_str)
            )
        self.Smult = int(components.Smult)
        self.S = (self.Smult - 1) / 2.0
        self.Lletter = components.Lletter
        self.L = atom_L_symbols.index(components.Lletter)
        self.parity = components.get("parity")
        self.moore_label = components.get("moore_label", "")
        try:
            self.J = parse_fraction(components.Jstr)
        except ValueError as err:
            raise AtomicTermSymbolError(err)
        if self.J is not None:
            self._validate_j()

    def _validate_j(self):
        s_is_half_integer = int(2 * self.S) % 2
        j_is_half_integer = int(2 * self.J) % 2
        if s_is_half_integer != j_is_half_integer:
            raise AtomicTermSymbolError(
                "J={} is invalid for S={}.".format(self.J, self.S)
            )
        if not abs(self.L - self.S) <= self.J <= self.L + self.S:
            raise AtomicTermSymbolError(
                "Invalid atomic term symbol: {0:s}"
                " |L-S| <= J <= L+S must be satisfied.".format(self.state_str)
            )

    @property
    def html(self):
        html_chunks = [
            "{0}<sup>{1:d}</sup>{2:s}".format(
                self.moore_label, self.Smult, self.Lletter
            )
        ]
        if self.parity:
            html_chunks.append("<sup>o</sup>")
        if self.J is not None:
            j_str = float_to_fraction(self.J)
            html_chunks.append("<sub>{0:s}</sub>".format(j_str))
        return "".join(html_chunks)

    @property
    def latex(self):
        latex_chunks = [
            r"{}{{}}^{{{}}}\mathrm{{{}}}".format(
                self.moore_label, self.Smult, self.Lletter
            )
        ]
        if self.parity:
            latex_chunks.append("^o")
        if self.J is not None:
            j_str = float_to_fraction(self.J)
            latex_chunks.append("_{{{}}}".format(j_str))
        return "".join(latex_chunks)

    def __repr__(self):
        return self.state_str
