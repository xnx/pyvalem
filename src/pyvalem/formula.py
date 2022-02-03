"""
This module defines the `Formula` class, representing a chemical formula (of an atom,
isotope, ion, molecule, molecular-ion, isotopologue, etc.) and associated
exceptions.

Quantum states are not defined in the `Formula` framework, for chemical species
with quantum states, look at the `StatefulSpecies` class.

Examples
--------
>>> from pyvalem.formula import Formula
>>> Formula("H2O+").charge
1

>>> dict(Formula("CH4").atom_stoich.items())
{'C': 1, 'H': 4}
"""

import re
from collections import defaultdict

import pyparsing as pp

from ._special_cases import special_cases
from .atom_data import element_symbols, atoms, isotopes

element = pp.oneOf(element_symbols)
# TODO: don't allow leading 0
integer = pp.Word(pp.nums)
integer_or_x = integer | pp.Literal("x")
plusminus = pp.Literal("+") | pp.Literal("-")

# An isotope looks like '(1H)', '(13C)', etc.; strip the parentheses.
isotope = (
    pp.Group(
        pp.Suppress(pp.Literal("(")) + integer + element + pp.Suppress(pp.Literal(")"))
    )
    | pp.Literal("D")
    | pp.Literal("T")
)

# some named components of a formula
# stoich comes before or after a "bare" element symbol, e.g. 3Br2.
pp_stoich = pp.Optional(integer_or_x, default="1").setResultsName("stoich")
# prestoich comes before a bracketed element group, e.g. 2(NH3).
pp_prestoich = pp.Optional(integer, default="1").setResultsName("prestoich")
# poststoich comes after a bracketed element group, e.g. (H2O)3.
pp_poststoich = pp.Optional(integer_or_x, default="1").setResultsName("poststoich")
# the charge is always defined and defaults to '0'.
pp_charge = pp.Optional(
    pp.Combine(pp.Group(plusminus + pp.Optional(integer, default="1"))), default="0"
).setResultsName("charge")
# An elementRef is either an element symbol or an isotope symbol plus a
# stoichiometry which is 1 if not given.
# NB check for element symbol first to catch Dy, Ti, etc. before parsing as
# hydrogen isotopes D or T.
elementRef = pp.Group((element | isotope).setResultsName("atom_symbol") + pp_stoich)
# A chemicalFormula is a series of elementRefs.
chemicalFormula = pp.Group(pp.OneOrMore(elementRef)).setResultsName("atoms")
# Radicals must be specified with the unicode character '·' (U+00B7).
radicalDot = pp.Optional("·").setResultsName("radical")

# A chargedChemicalFormula is a chemicalFormula with an optional pre-
# stoichiometry, radical dot and charge.
chargedChemicalFormula = pp.Group(pp_stoich + chemicalFormula + radicalDot + pp_charge)

# A bracketedChemicalFormula is essentially a chargedChemicalFormula inside
# parentheses with optional pre- and post-stoichiometries.
left_bracket = pp.Literal("(")
right_bracket = pp.Literal(")")
bracketedChemicalFormula = pp.Group(
    pp_prestoich
    + pp.Suppress(left_bracket)
    + chemicalFormula
    + radicalDot
    + pp_charge
    + pp.Suppress(right_bracket)
    + pp_poststoich
)

# A chemical_formula_fragment is either one of the above ChemicalFormula
# types, optionally prefixed with a period ('.')
chemical_formula_fragment = pp.Optional(pp.Suppress(".")) + (
    chargedChemicalFormula | bracketedChemicalFormula
)
chemical_formula_fragments = pp.OneOrMore(chemical_formula_fragment).setResultsName(
    "formula"
)

# These are the formula prefix tokens we recognise and their slugs
# NB be careful to ensure that the slugs remain case-insensitive!
# For example, '(S)-' -> 'S-' but 's-' -> 'syn-'
prefix_tokens = {
    "(+)": "p",
    "(-)": "m",
    "(±)": "pm",
    "D": "D",
    "L": "L",
    "(R)": "R",
    "(S)": "S",
    "(E)": "E",
    "(Z)": "Z",
    "c": "c",
    "l": "l",
    "cis": "cis",
    "trans": "trans",
    "s": "syn",
    "a": "anti",
    "Δ": "Delta",
    "Λ": "Lambda",
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "n": "n",
    "i": "i",
    "t": "t",
    "neo": "neo",
    "sec": "sec",
    "o": "o",
    "m": "m",
    "p": "p",
    "ortho": "ortho",
    "meta": "meta",
    "para": "para",
}
# The LaTeX equivalents of these prefix tokens.
latex_prefix_dict = {
    "(±)": r"\pm",
    "Δ": r"\Delta",
    "Λ": r"\Lambda",
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
}

# also allow a comma-separated list of integers, e.g. 1,1,2-
prefix_parser = pp.delimitedList(pp.OneOrMore(integer), combine=True)
keys_list = list(prefix_tokens.keys())
for pt in keys_list:
    prefix_parser |= pp.Keyword(pt)
# Any number of prefix tokens may appear, separated by a hyphen
prefix_list_parser = (
    pp.delimitedList(prefix_parser, delim="-") + pp.Suppress(pp.Literal("-"))
).setResultsName("prefix")

# Finally, a complexChemicalFormula is a prefix, followed by one or more
# chemical_formula_fragments.
complexChemicalFormula = (
    pp.Optional(prefix_list_parser)
    + chemical_formula_fragments
    + pp_charge
    + pp.StringEnd()
)
# replace '+' and '-' with 'p' and 'm' to make slugs for e.g. URLs.
slug_charge_sign = {"+": "p", "-": "m"}


class FormulaError(Exception):
    pass


class FormulaParseError(FormulaError):
    pass


class Formula:
    """A class representing a chemical formula without states.

    Methods are implemented for the `Formula` from a compatible string and providing
    *html* and *LaTeX* representations, atomic stoichiometry, species mass, number of
    atoms, or html-save slug.

    Parameters
    ----------
    formula : str
        PyValem-compatible string. No ``"_"`` or ``"^"`` symbols to indicate subscripts
        and superscripts. Brackets are allowed, as well as several common prefixes.
        Charges are provided by ``"+"/"-"``, or ``"+n"/"-n"``, where `n` is the charge

    Attributes
    ----------
    formula : str
        The formula string as passed to the constructor.
    atoms : set of `Atom`
    atom_stoich : dict[str, int]
    charge : int
        Charge in [e].
    natoms : int
        Number of atoms of the `Formula`.
    rmm, mass : float
        Both are the mass in [amu] (one is alias for the other).
    html, latex, slug : str
        Different string representations of the `Formula`. The ``slug`` is a url-safe
        representation.

    Raises
    ------
    FormulaParseError
        When an incompatible `formula` string is passed into the constructor

    Notes
    -----
    The ``__repr__`` method is overloaded to provide a *canonicalised* representation
    of the formula. The idea is that two formulas representing the same physical entity
    will have the same ``repr(formula)`` representation.

    Examples
    --------
    >>> Formula("H2+")  # a simple chemical formula instantiation
    H2+

    >>> Formula("(1H)2(16O)")  # isotopologue instantiation
    (1H)2(16O)

    >>> Formula("ortho-C6H4(CH3)2"), Formula("W+42")  # more complicated situations
    (ortho-C6H4(CH3)2, W+42)

    >>> # Attributes available:
    >>> dict(Formula("CH4").atom_stoich)
    {'C': 1, 'H': 4}
    >>> Formula("(2H)(3H)+").html
    '<sup>2</sup>H<sup>3</sup>H<sup>+</sup>'
    >>> Formula("Ar").mass
    39.95

    >>> # Incompatible formula string
    >>> Formula("Argon")
    Traceback (most recent call last):
    ...
    pyvalem.formula.FormulaParseError: Invalid formula syntax: Argon
    """

    def __init__(self, formula):
        """Initialize the Formula object by parsing the string argument formula."""
        self.formula = formula
        self.atoms = set()
        self.atom_stoich = defaultdict(int)
        self.charge = 0
        self.natoms = 0
        self.rmm = 0.0
        self.html = ""
        self.latex = ""
        self.slug = ""
        self.mass = 0.0
        self._parse_formula(formula)

    @staticmethod
    def _make_prefix_html(prefix_list):
        """Make the prefix HTML: D- and L- prefixes get written in small caps"""
        prefix = "-".join(prefix_list)
        prefix = prefix.replace("D", '<span style="font-size: 80%;">D</span>')
        prefix = prefix.replace("L", '<span style="font-size: 80%;">L</span>')
        return "{}-".format(prefix)

    @staticmethod
    def _make_prefix_latex(prefix_list):
        """Make the prefix LaTeX."""
        latex_prefixes = [latex_prefix_dict.get(pr, pr) for pr in prefix_list]
        prefix = "-".join(latex_prefixes)
        return "{}-".format(prefix)

    @staticmethod
    def _make_prefix_slug(prefix_list):
        """Make the prefix slug

        Commas are replaced by underscores and non-ASCII
        characters swapped out according to the entries in the prefix_tokens
        dictionary. For example,
            1,1,3- -> 1_1_3-
            (±)- -> pm-
            (α)- -> alpha-
        """
        slug_prefix_tokens = []
        for prefix_token in prefix_list:
            # TODO don't allow matches including numbers with leading zeros
            if re.match(r"^\d+(,\d+)*$", prefix_token):
                # this prefix token is a comma-separated list of numbers
                slug_prefix_token = prefix_token.replace(",", "_")
            else:
                # select the slug version of this prefix from prefix_tokens
                try:
                    slug_prefix_token = prefix_tokens[prefix_token]
                except KeyError:
                    raise FormulaParseError(
                        "Unrecognised formula prefix" " token: {}".format(prefix_token)
                    )
            slug_prefix_tokens.append(slug_prefix_token)
        slug_prefix = "_".join(slug_prefix_tokens)
        return "{}__".format(slug_prefix)

    def _parse_formula(self, formula):
        """Parse the formula string into a Formula object.

        The main method of the class, populates all the instance attributes.

        Parameters
        ----------
        formula : str
            See the class docstring.

        Raises
        ------
        FormulaParseError
        """
        if formula == "D-":
            # This is a not-ideal way to deal with the fact that D- breaks
            # the parser due to a clash with the D- prefix.
            self._parse_formula("D-1")
            return

        if any(s in formula for s in ("++", "--", "+-", "-+")):
            raise FormulaParseError("Invalid formula syntax: {}".format(formula))

        # We make a particular exception for various special cases, including
        # photons, electrons, positrons and "M", denoting an unspecified
        # "third-body" in many reactions. Note that M does not have a defined
        # charge or mass.
        if formula == "e":
            # Quietly convert e to e-.
            self.formula = formula = "e-"
        if formula in special_cases:
            for attr, val in special_cases[formula].items():
                setattr(self, attr, val)
            return

        try:
            moieties = complexChemicalFormula.parseString(formula)
        except pp.ParseException:
            raise FormulaParseError("Invalid formula syntax: %s" % formula)

        html_chunks = []
        latex_chunks = []
        slug_chunks = []
        # calculate relative molecular mass as the sum of the atomic weights

        # make the prefix html and slug
        if "prefix" in moieties.keys():
            html_chunks.append(self._make_prefix_html(moieties["prefix"]))
            latex_chunks.append(self._make_prefix_latex(moieties["prefix"]))
            slug_chunks.append(self._make_prefix_slug(moieties["prefix"]))

        moieties, total_charge = moieties["formula"], int(moieties["charge"])
        nmoieties = len(moieties)
        for i, moiety in enumerate(moieties):
            poststoich = 0
            if "prestoich" in moiety.keys():
                # bracketed fragment, e.g. (OH)2, 3(HO2+), ...
                prestoich = int(moiety["prestoich"])
                if prestoich > 1:
                    slug_chunks.append(moiety["prestoich"])
                    html_chunks.append(moiety["prestoich"])
                    latex_chunks.append(moiety["prestoich"])
                html_chunks.append("(")
                latex_chunks.append("(")
                slug_chunks.append("_l_")
                poststoich = int(moiety["poststoich"])
                stoich = prestoich * poststoich
            else:
                # unbracketed fragment, e.g. H2O, 2NH3, ...
                stoich = int(moiety["stoich"])
                if stoich > 1:
                    slug_chunks.append(moiety["stoich"])
                    html_chunks.append(moiety["stoich"])
                    latex_chunks.append(moiety["stoich"])
            charge = int(moiety["charge"])
            self.charge += charge * stoich
            for atom in moiety["atoms"]:
                atom_symbol, atom_stoich = atom

                if atom_symbol == "D":
                    atom_symbol = isotope.parseString("(2H)")[0]
                if atom_symbol == "T":
                    atom_symbol = isotope.parseString("(3H)")[0]
                if isinstance(atom_symbol, pp.ParseResults):
                    # we got an isotope in the form '(zSy)' with z the mass
                    # number so symbol is the ParseResults ['z', 'Sy']:
                    mass_number, atom_symbol = (int(atom_symbol[0]), atom_symbol[1])
                    symbol_html = "<sup>%d</sup>%s" % (mass_number, atom_symbol)
                    symbol_latex = r"^{{{0:d}}}\mathrm{{{1:s}}}".format(
                        mass_number, atom_symbol
                    )
                    atom_symbol = "%d%s" % (mass_number, atom_symbol)
                    slug_chunks.append("-%s" % atom_symbol)
                else:
                    mass_number = None
                    symbol_html = atom_symbol
                    symbol_latex = r"\mathrm{{{0:s}}}".format(atom_symbol)
                    slug_chunks.append(atom_symbol)

                if mass_number is not None:
                    # We have an isotope, specified as '(zSy)'.
                    try:
                        atom = isotopes[atom_symbol]
                    except KeyError:
                        raise FormulaParseError(
                            "Unknown isotope symbol"
                            " {} in formula {}".format(atom_symbol, formula)
                        )
                else:
                    # A regular element symbol for an atom.
                    try:
                        atom = atoms[atom_symbol]
                    except KeyError:
                        raise FormulaParseError(
                            "Unknown element symbol"
                            " {} in formula {}".format(atom_symbol, formula)
                        )

                self.atoms.add(atom)

                try:
                    i_atom_stoich = int(atom_stoich)
                    total_atom_stoich = i_atom_stoich * stoich
                    self.natoms += total_atom_stoich
                    try:
                        self.rmm += atom.mass * total_atom_stoich
                    except TypeError:
                        # No atomic weight for some elements (e.g. Tc, Pm)
                        self.rmm = None
                except ValueError:
                    # Some formulas don't have well-defined stoichiometries,
                    # e.g. 'CFx'
                    total_atom_stoich = None
                    self.natoms = self.rmm = None
                try:
                    self.atom_stoich[atom_symbol] += total_atom_stoich
                except TypeError:
                    # There's not much we can do for the stoichiometry if this
                    # atom occurs with an undefined value.
                    # noinspection PyTypeChecker
                    self.atom_stoich[atom_symbol] = None

                html_chunks.append(symbol_html)
                latex_chunks.append(symbol_latex)
                if atom_stoich != "1":
                    html_chunks.append("<sub>{}</sub>".format(atom_stoich))
                    latex_chunks.append("_{{{0}}}".format(atom_stoich))
                    slug_chunks.append(str(atom_stoich))

            (
                moiety_charge_html,
                moiety_charge_latex,
                moiety_charge_slug,
            ) = self._get_charge_reps(charge)
            html_chunks.append(moiety_charge_html)
            latex_chunks.append(moiety_charge_latex)
            slug_chunks.append(moiety_charge_slug)
            # if i < nmoieties-1 and nmoieties != 1:
            #    slug_chunks.append('_d_')

            if "poststoich" in moiety.keys():
                html_chunks.append(")")
                latex_chunks.append(")")
                slug_chunks.append("_r_")
                # if i == nmoieties and nmoieties != 1:
                #    slug_chunks.append('_d_')
                if poststoich > 1:
                    html_chunks.append("<sub>{:d}</sub>".format(poststoich))
                    latex_chunks.append("_{{{0:d}}}".format(poststoich))
                    slug_chunks.append("{:d}".format(poststoich))

            if "radical" in moiety.keys():
                html_chunks.append("&#183;")
                latex_chunks.append(r"\cdot")
                slug_chunks.append("_dot")
            if i != nmoieties - 1:
                slug_chunks.append("-")

        if total_charge:
            # TODO Refactor and test further
            self.charge = int(total_charge)
            (
                moiety_charge_html,
                moiety_charge_latex,
                moiety_charge_slug,
            ) = self._get_charge_reps(self.charge)
            html_chunks.append(moiety_charge_html)
            latex_chunks.append(moiety_charge_latex)
            slug_chunks.append(moiety_charge_slug)

        self.html = "".join(html_chunks)
        self.latex = "".join(latex_chunks)
        # strip the leading '-' if the formula began with an isotope
        self.slug = "".join(slug_chunks).lstrip("-")

        self.mass = self.rmm

    @staticmethod
    def _get_charge_reps(charge):
        if charge:
            s_charge = ""
            if abs(charge) > 1:
                s_charge = str(abs(charge))
            s_charge_sign = "+"
            if charge < 0:
                s_charge_sign = "-"
            moiety_charge_html = "<sup>{:s}{:s}</sup>".format(s_charge, s_charge_sign)
            moiety_charge_latex = "^{{{0:s}{1:s}}}".format(s_charge, s_charge_sign)
            moiety_charge_slug = "_{:s}{:s}".format(
                slug_charge_sign[s_charge_sign], s_charge
            )
            return moiety_charge_html, moiety_charge_latex, moiety_charge_slug
        return "", "", ""

    def __repr__(self):
        if self.formula == "hv":
            return "hν"
        return self.formula

    def __eq__(self, other):
        return repr(self.formula) == repr(other.formula)

    def _stoichiometric_formula_atomic_number(self):
        """Return a list of atoms/isotopes and their stoichiometries.

        The returned list is sorted in order of increasing atomic number.
        """

        atom_strs = []
        for atom in sorted(self.atoms, key=lambda e: (e.Z, e.mass)):
            if atom.is_isotope:
                symbol = "({})".format(atom.symbol)
            else:
                symbol = atom.symbol
            atom_strs.append(
                self._get_symbol_stoich(symbol, self.atom_stoich[atom.symbol])
            )
        return atom_strs

    def _stoichiometric_formula_alphabetical(self):
        """Return a list of atoms/isotopes and their stoichiometries.

        The returned list is sorted in alphabetical order.
        """
        atom_strs = self._stoichiometric_formula_atomic_number()
        atom_strs.sort()
        return atom_strs

    def _stoichiometric_formula_hill(self):
        """Return a list of atoms/isotopes and their stoichiometries.

        The returned list is sorted in "Hill notation": first carbon, then
        hydrogen, then all other chemical elements in alphabetical order.
        If the species contains H but no C, all elements are listed in
        alphabetical order, including hydrogen.
        """
        c_h_strs = []
        atom_strs = []
        contains_c = False
        for atom in sorted(self.atoms, key=lambda e: (e.Z, e.mass)):
            if atom.is_isotope:
                symbol = "({})".format(atom.symbol)
            else:
                symbol = atom.symbol
            if symbol == "C":
                c_h_strs.insert(0, self._get_symbol_stoich("C", self.atom_stoich["C"]))
                contains_c = True
            elif symbol == "H":
                c_h_strs.insert(1, self._get_symbol_stoich("H", self.atom_stoich["H"]))
            else:
                atom_strs.append(
                    self._get_symbol_stoich(symbol, self.atom_stoich[atom.symbol])
                )

        if not contains_c:
            atom_strs = c_h_strs + atom_strs
            c_h_strs = []
        atom_strs.sort()
        return c_h_strs + atom_strs

    def stoichiometric_formula(self, fmt="atomic number"):
        """Return a string representation of the stoichiometric formula.

        The formula is given in one of the formats specified by the fmt argument:
        "atomic number": order atoms by increasing atomic number
        "alphabetical" : order atoms in alphabetical order of atomic symbol
        "hill": first C, then H, then all other chemical elements in alphabetical order,
                if C not present, all alphabetical.

        Parameters
        ----------
        fmt : {"atomic number", "alphabetical", "hill"}

        Returns
        -------
        str
            Stoichiometric formula (with charges)

        Examples
        --------
        >>> Formula("L-CH3CH(NH2)CO2H").stoichiometric_formula("atomic number")
        'H7C3NO2'

        >>> Formula("L-CH3CH(NH2)CO2H+").stoichiometric_formula("alphabetical")
        'C3H7NO2+'
        """
        # Special cases
        if self.formula in {"M", "e-", "e+"}:
            return self.formula
        if self.formula in {"hv", "hν"}:
            # Special case for the photon
            return "hν"

        fmt = fmt.lower()
        if fmt == "atomic number":
            atom_strs = self._stoichiometric_formula_atomic_number()
        elif fmt == "alphabetical":
            atom_strs = self._stoichiometric_formula_alphabetical()
        elif fmt == "hill":
            atom_strs = self._stoichiometric_formula_hill()
        else:
            raise FormulaError(
                "Unsupported format for stoichiometric formula output: {}".format(fmt)
            )

        # finally, add on the charge string, e.g. '', '-', '+2', ...
        atom_strs.append(self._get_charge_string())
        return "".join(atom_strs)

    @staticmethod
    def _get_symbol_stoich(symbol, stoich):
        """Return Xn for element symbol X and stoichiometry n, unless n is 1,
        in which case, just return X.
        """
        if stoich is None:
            return "{}x".format(symbol)
        if stoich > 1:
            return "{}{:d}".format(symbol, stoich)
        return symbol

    def _get_charge_string(self):
        """Return the string representation of the charge: '+', '-', '+2', '-3', etc."""
        if not self.charge:
            return ""
        if self.charge > 0:
            if self.charge > 1:
                return "+{:d}".format(self.charge)
            return "+"
        if self.charge == -1:
            return "-"
        return str(self.charge)
