"""
The RacahSymbol class, for the representation of an atomic state in Racah
notation, with methods for parsing a string into quantum numbers and
labels, creating an HTML representation of the term symbol, etc.
"""

import pyparsing as pp

from pyvalem.states._base_state import State, StateParseError

integer = pp.Word(pp.nums)
atom_principal = integer.setResultsName("principal")

orbital_labels = ("s", "s'", "p", "p'", "d", "d'", "f", "f'")
atom_orbital = pp.oneOf(orbital_labels).setResultsName("orbital")
parity_label = pp.Literal("o").setResultsName("parity")

atom_k_term = (
    integer.setResultsName("k_num") + pp.Suppress("/") + integer.setResultsName("k_den")
)

atom_j_term = integer.setResultsName("jterm")

racah_symbol_template = (
    atom_principal
    + atom_orbital
    + pp.Suppress("[")
    + atom_k_term
    + pp.Suppress("]")
    + pp.Optional(parity_label)
    + pp.Optional("_" + atom_j_term)
)


class RacahSymbol(State):
    """
    The RacahSymbol class representing an atomic state in Racah notation.

    This class is currently little more than a stub. The term symbol of the
    parent configuration must be specified as a separate State; this class
    defines nl[K]_J, where _J is optional to allow for the case where a
    state is an average over J levels.
    """

    def __init__(self, state_str):
        self.state_str = state_str
        self.principal = None
        self.orbital = None
        self.parent_rot = None
        self.k_num = None
        self.k_den = None
        self.j_term = None
        self.parity = None
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        try:
            components = racah_symbol_template.parseString(state_str)
        except pp.ParseException:
            raise StateParseError("Invalid Racah notation syntax: {}".format(state_str))
        self.principal = int(components.principal)
        self.orbital = components.orbital
        if "'" in self.orbital:
            self.parent_rot = 0.5
        else:
            self.parent_rot = 1.5
        self.k_num = int(components.k_num)
        self.k_den = int(components.k_den)
        self.parity = "o" if components.parity else ""
        if components.jterm != "":
            self.j_term = int(components.jterm)

    def __repr__(self):
        parent = f"{self.principal}{self.orbital}"
        k = f"{self.k_num}/{self.k_den}"
        s_jterm = f"_{self.j_term}" if self.j_term is not None else ""
        return f"{parent}[{k}]{self.parity}{s_jterm}"

    @property
    def html(self):
        parent = f"{self.principal}{self.orbital}"
        k = f"{self.k_num}/{self.k_den}"
        s_parity = "<sup>o</sup>" if self.parity else ""
        s_jterm = f"<sub>{self.j_term}</sub>" if self.j_term is not None else ""
        return f"{parent}[{k}]{s_parity}{s_jterm}"
