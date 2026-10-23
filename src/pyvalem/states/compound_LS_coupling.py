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

from pyvalem.states._base_state import (
    State,
    StateParseError,
    StateValidationError,
)

from .atomic_configuration import AtomicConfiguration, AtomicConfigurationError
from .atomic_term_symbol import AtomicTermSymbol, AtomicTermSymbolError

term_patt = r"\((.*?)\)"


class CompoundLSCouplingError(StateParseError):
    pass


class CompoundLSCouplingValidationError(CompoundLSCouplingError, StateValidationError):
    pass


class CompoundLSCoupling(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.atomic_configurations = []
        self.terms = []
        self._parse_state(self.state_str)

    @property
    def term_symbols(self):
        """The intermediate terms: an alias for `terms`."""
        return self.terms

    def _parse_state(self, state_str):
        invalid_syntax = "Invalid compound LS coupling syntax: {}".format(state_str)
        terms = re.findall(term_patt, state_str)
        configs = state_str.split("(")

        if len(configs) == 0 or len(terms) == 0:
            raise CompoundLSCouplingError(invalid_syntax)

        try:
            for i in range(1, len(configs)):
                configs[i] = configs[i][len(terms[i - 1]) + 1 :]
        except IndexError as err:
            raise CompoundLSCouplingError(invalid_syntax) from err

        if not configs[-1]:
            configs = configs[:-1]

        try:
            self.terms = [AtomicTermSymbol(term) for term in terms]
            self.atomic_configurations = [
                AtomicConfiguration(config) for config in configs
            ]
        except (AtomicTermSymbolError, AtomicConfigurationError) as err:
            if isinstance(err, StateValidationError):
                error_class = CompoundLSCouplingValidationError
            else:
                error_class = CompoundLSCouplingError
            raise error_class(
                "Invalid compound LS coupling state {}: {}".format(state_str, err)
            ) from err

    def __repr__(self):
        return self.state_str

    @property
    def html(self):
        html_chunks = []
        for config, term in zip(self.atomic_configurations, self.terms, strict=False):
            html_chunks.append(config.html)
            html_chunks.append(f"({term.html})")
        if len(self.atomic_configurations) > len(self.terms):
            html_chunks.append(self.atomic_configurations[-1].html)
        return "".join(html_chunks)

    @property
    def latex(self):
        latex_chunks = []
        for config, term in zip(self.atomic_configurations, self.terms, strict=False):
            latex_chunks.append(config.latex)
            latex_chunks.append(f"({term.latex})")
        if len(self.atomic_configurations) > len(self.terms):
            latex_chunks.append(self.atomic_configurations[-1].latex)
        return "".join(latex_chunks)
