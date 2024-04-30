"""
The CompoundLSCoupling class, representing a complex atomic state with
multiple configurations coupling within the LS formulism to several
intermediate terms, e.g. "4f(2Fo)5d2(1G)6s(2G)". The final term should
be given as its own AtomicTermSymbol. The full CompoundLSCoupling state
should contain no spaces; NB the different interaction strength cases
detailed in Martin et al. (sec. 11.8.1) are not yet implemented.

W. C. Martin, W. Wiese, A. Kramida, "Atomic Spectroscopy" in "Springer
Handbook of Atomic, Molecular and Optical Physics", G. W. F. Drake (ed.),
https://doi.org/10.1007/978-3-030-73893-8_11

Includes methods for parsing a string into quantum numbers and labels,
creating an HTML representation of the term symbol, etc.
"""

import re

from pyvalem.states._base_state import State, StateParseError
from .atomic_term_symbol import AtomicTermSymbol, AtomicTermSymbolError
from .atomic_configuration import AtomicConfiguration, AtomicConfigurationError

term_patt = r"\((.*?)\)"


class CompoundLSCouplingError(StateParseError):
    pass


class CompoundLSCoupling(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.atomic_configurations = []
        self.term_symbols = []
        self._parse_state(self.state_str)

    def _parse_state(self, state_str):
        terms = re.findall(term_patt, state_str)
        configs = state_str.split("(")

        if len(configs) == 0 or len(terms) == 0:
            raise CompoundLSCouplingError

        try:
            for i, config in enumerate(configs[1:], start=1):
                configs[i] = configs[i][len(terms[i - 1]) + 1 :]
        except IndexError:
            raise CompoundLSCouplingError

        if not configs[-1]:
            configs = configs[:-1]

        try:
            self.terms = [AtomicTermSymbol(term) for term in terms]
            self.atomic_configurations = [
                AtomicConfiguration(config) for config in configs
            ]
        except (AtomicTermSymbolError, AtomicConfigurationError):
            raise CompoundLSCouplingError

    def __repr__(self):
        return self.state_str

    @property
    def html(self):
        html_chunks = []
        for config, term in zip(self.atomic_configurations, self.terms):
            html_chunks.append(config.html)
            html_chunks.append(f"({term.html})")
        if len(self.atomic_configurations) > len(self.terms):
            html_chunks.append(self.atomic_configurations[-1].html)
        return "".join(html_chunks)

    @property
    def latex(self):
        latex_chunks = []
        for config, term in zip(self.atomic_configurations, self.terms):
            latex_chunks.append(config.latex)
            latex_chunks.append(f"({term.latex})")
        if len(self.atomic_configurations) > len(self.terms):
            latex_chunks.append(self.atomic_configurations[-1].latex)
        return "".join(latex_chunks)
