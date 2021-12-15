"""
The DiatomicMolecularConfiguration class, representing a diatomic molecular
configuration with methods for parsing a string into quantum numbers and
labels, creating an HTML representation of the term symbol, etc.
"""

import pyparsing as pp

from .atomic_configuration import atomic_orbital_symbols
from .state import State, StateParseError

integer = pp.Word(pp.nums)
molecular_orbital_symbols = (
    "σ",
    "π",
    "δ",
    "sigma",
    "pi",
    "delta",
    "σg",
    "πg",
    "δg",
    "σu",
    "πu",
    "δu",
    "sigmag",
    "pig",
    "deltag",
    "sigmau",
    "piu",
    "deltau",
)

greek_letters = {
    "sigma": "σ",
    "pi": "π",
    "delta": "δ",
    "sigmag": "σg",
    "sigmau": "σu",
    "pig": "πg",
    "piu": "πu",
    "deltag": "δg",
    "deltau": "δu",
}
symbol_latex = {"σ": r"\sigma", "π": r"\pi", "δ": r"\delta"}

molecule_orbital = pp.Group(
    integer.setResultsName("n")
    + pp.oneOf(molecular_orbital_symbols).setResultsName("symbol")
    + pp.Optional(integer.setResultsName("count"), default="1")
)

molecule_config = (
    molecule_orbital
    + pp.ZeroOrMore(pp.Suppress(".") + molecule_orbital)
    + pp.StringEnd()
).leaveWhitespace()

# atomic_orbital = pp.Group(integer.setResultsName('n') +
#                    pp.oneOf(atomic_orbital_symbols).setResultsName('lletter')
#                         )
alt_molecule_orbital = pp.Group(
    integer.setResultsName("n")
    + pp.oneOf(atomic_orbital_symbols).setResultsName("lletter")
    + pp.Suppress("-")
    + pp.oneOf(molecular_orbital_symbols).setResultsName("symbol")
    + pp.Optional(integer.setResultsName("count"), default="1")
)
alt_molecule_config = (
    alt_molecule_orbital
    + pp.ZeroOrMore(pp.Suppress(".") + alt_molecule_orbital)
    + pp.StringEnd()
).leaveWhitespace()


class DiatomicMolecularOrbitalError(StateParseError):
    pass


class DiatomicMolecularConfigurationError(StateParseError):
    pass


class DiatomicMolecularOrbital:
    def __init__(self, n, symbol, count):
        self.n = int(n)
        if symbol in greek_letters.keys():
            self.symbol = greek_letters[symbol]
        else:
            self.symbol = symbol
        self.count = int(count)
        self.validate_molecular_orbital()

    def __repr__(self):
        return "{:d}{:s}{:d}".format(self.n, self.symbol, self.count)

    def __hash__(self):
        return hash((self.n, self.symbol, self.count))

    def __eq__(self, other):
        return (
            self.n == other.n
            and self.symbol == other.symbol
            and self.count == other.count
        )

    def validate_molecular_orbital(self):
        if self.symbol == "σ":
            if self.count > 2:
                raise DiatomicMolecularOrbitalError(
                    "Only two electrons"
                    " allowed in σ orbital, but received {:d}".format(self.count)
                )
        else:
            if self.count > 4:
                raise DiatomicMolecularOrbitalError(
                    "Only four electrons"
                    " allowed in π and δ orbitals, "
                    "but received {:d}".format(self.count)
                )

    @staticmethod
    def _make_symbol_html(symbol):
        if symbol[-1] in "ug":
            return symbol[:-1] + "<sub>{}</sub>".format(symbol[-1])
        return symbol

    @property
    def html(self):
        return "{:d}{:s}<sup>{:d}</sup>".format(
            self.n, self._make_symbol_html(self.symbol), self.count
        )

    @staticmethod
    def _make_symbol_latex(symbol):
        if symbol[-1] in "ug":
            return symbol_latex[symbol[:-1]] + "_{}".format(symbol[-1])
        return symbol_latex[symbol]

    @property
    def latex(self):
        return "{:d}{:s}^{{{:d}}}".format(
            self.n, self._make_symbol_latex(self.symbol), self.count
        )


class AltDiatomicMolecularOrbital(DiatomicMolecularOrbital):
    """
    Alternative syntax for diatomic molecular orbitals: e.g. 1s-σg2.1s-σu1

    """

    def __init__(self, n, lletter, symbol, count):
        self.lletter = lletter
        super().__init__(n, symbol, count)

    def __repr__(self):
        return "{}{}-{}{}".format(self.n, self.lletter, self.symbol, self.count)

    def __hash__(self):
        return hash((self.n, self.lletter, self.symbol, self.count))

    def __eq__(self, other):
        return (
            self.n == self.n
            and self.lletter == self.lletter
            and self.symbol == self.symbol
            and self.count == self.count
        )

    @property
    def html(self):
        return "{:d}{}{:s}<sup>{:d}</sup>".format(
            self.n, self.lletter, self._make_symbol_html(self.symbol), self.count
        )

    @property
    def latex(self):
        return "{:d}{}{:s}^{{{:d}}}".format(
            self.n, self.lletter, self._make_symbol_latex(self.symbol), self.count
        )


class DiatomicMolecularConfiguration(State):
    def __init__(self, state_str):
        self.state_str = state_str
        self.orbitals = []
        self.parse_state(state_str)

    def parse_state(self, state_str):
        if "-" in state_str:
            self.parse_alt_config(state_str)
        else:
            self.parse_regular_config(state_str)

    def parse_regular_config(self, state_str):
        try:
            parse_results = molecule_config.parseString(state_str)
        except pp.ParseException:
            raise DiatomicMolecularConfigurationError(
                "Invalid diatomic molecular electronic "
                "configuration syntax: {0}".format(state_str)
            )

        for i, parsed_orbital in enumerate(parse_results):
            try:
                temp_orbital = DiatomicMolecularOrbital(
                    n=parsed_orbital["n"],
                    symbol=parsed_orbital["symbol"],
                    count=parsed_orbital["count"],
                )
            except DiatomicMolecularOrbitalError as err:
                raise DiatomicMolecularConfigurationError(err)
            self.orbitals.append(temp_orbital)
        self.validate_configuration()

    def parse_alt_config(self, state_str):
        try:
            parse_results = alt_molecule_config.parseString(state_str)
        except pp.ParseException:
            raise DiatomicMolecularConfigurationError(
                "Invalid diatomic molecular electronic "
                "configuration syntax: {0}".format(state_str)
            )

        self.orbitals = []
        for i, parsed_orbital in enumerate(parse_results):
            try:
                temp_orbital = AltDiatomicMolecularOrbital(
                    n=parsed_orbital["n"],
                    lletter=parsed_orbital["lletter"],
                    symbol=parsed_orbital["symbol"],
                    count=parsed_orbital["count"],
                )
            except DiatomicMolecularOrbitalError as err:
                raise DiatomicMolecularConfigurationError(err)
            self.orbitals.append(temp_orbital)
        self.validate_alt_configuration()

    def validate_configuration(self):
        orbitals = [(o.n, o.symbol) for o in self.orbitals]
        if len(orbitals) != len(set(orbitals)):
            raise DiatomicMolecularConfigurationError(
                "Repeated orbitals " "in {0}".format(self.state_str)
            )

    def validate_alt_configuration(self):
        orbitals = [(o.n, o.lletter, o.symbol) for o in self.orbitals]
        if len(orbitals) != len(set(orbitals)):
            raise DiatomicMolecularConfigurationError(
                "Repeated orbitals " "in {0}".format(self.state_str)
            )

    def __repr__(self):
        return ".".join([str(orbital) for orbital in self.orbitals])

    def __hash__(self):
        return hash(self.state_str)

    @property
    def html(self):
        html_chunks = []
        if self.orbitals:
            for orbital in self.orbitals:
                html_chunks.append(orbital.html)
        return ".".join(html_chunks)

    @property
    def latex(self):
        latex_chunks = []
        if self.orbitals:
            for orbital in self.orbitals:
                latex_chunks.append(orbital.latex)
        return "".join(latex_chunks)

    def __eq__(self, other):
        return self.orbitals == other.orbitals
