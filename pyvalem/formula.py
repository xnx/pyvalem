"""
Defines the Formula class, representing a chemical formula (of an atom,
isotope, ion, molecule, molecular-ion, isotopologue, etc.) and associated
exceptions.
"""

import sys
import re
from collections import defaultdict
import pyparsing as pp
from .atom_data import element_symbols, atoms, isotopes
from .special_cases import special_cases

element = pp.oneOf(element_symbols)
# TODO don't allow leading 0
integer = pp.Word(pp.nums)
integer_or_x = integer | pp.Literal('x')
plusminus = pp.Literal('+') | pp.Literal('-')

# An isotope looks like '(1H)', '(13C)', etc.; strip the parentheses.
isotope = ( pp.Group(pp.Suppress(pp.Literal('(')) + integer + element
                + pp.Suppress(pp.Literal(')')))
            | pp.Literal('D') | pp.Literal('T')
          )

# some named components of a formula
# stoich comes before or after a "bare" element symbol, e.g. 3Br2.
stoich = pp.Optional(integer_or_x, default='1').setResultsName('stoich')
# prestoich comes before a bracketed element group, e.g. 2(NH3).
prestoich = pp.Optional(integer, default='1').setResultsName('prestoich')
# poststoich comes after a bracketed element group, e.g. (H2O)3.
poststoich = pp.Optional(integer_or_x, default='1'
                                            ).setResultsName('poststoich')
# the charge is always defined and defaults to '0'.
charge = pp.Optional(pp.Combine(pp.Group(plusminus + pp.Optional(integer,
                        default='1'))), default='0').setResultsName('charge')
# An elementRef is either an element symbol or an isotope symbol plus a
# stoichiometry which is 1 if not given.
# NB check for element symbol first to catch Dy, Ti, etc. before parsing as
# hydrogen isotopes D or T.
elementRef = pp.Group((element | isotope).setResultsName('atom_symbol')+stoich)
# A chemicalFormula is a series of elementRefs.
chemicalFormula = pp.Group(pp.OneOrMore(elementRef)).setResultsName('atoms')
# Radicals must be specified with the unicode character '·' (U+00B7).
radicalDot = pp.Optional('·').setResultsName('radical')

# A chargedChemicalFormula is a chemicalFormula with an optional pre-
# stoichiometry, radical dot and charge.
chargedChemicalFormula= pp.Group(stoich + chemicalFormula + radicalDot
                                        + charge)

# A bracketedChemicalFormula is essentially a chargedChemicalFormula inside
# parentheses with optional pre- and post-stoichiometries.
left_bracket = pp.Literal('(')
right_bracket = pp.Literal(')')
bracketedChemicalFormula = pp.Group(prestoich + pp.Suppress(left_bracket)
                         + chemicalFormula + radicalDot + charge
                         + pp.Suppress(right_bracket) + poststoich)

# A chemical_formula_fragment is either one of the above ChemicalFormula
# types, optionally prefixed with a period ('.')
chemical_formula_fragment = pp.Optional(pp.Suppress('.'))\
            + (chargedChemicalFormula | bracketedChemicalFormula)
chemical_formula_fragments = pp.OneOrMore(chemical_formula_fragment)\
                            .setResultsName('formula')

# These are the formula prefix tokens we recognise and their slugs
# NB be careful to ensure that the slugs remain case-insensitive!
# For example, '(S)-' -> 'S-' but 's-' -> 'syn-'
prefix_tokens = {'(+)': 'p', '(-)': 'm', '(±)': 'pm', 'D': 'D', 'L': 'L',
                 '(R)': 'R', '(S)': 'S', '(E)': 'E', '(Z)': 'Z',
                 'c':'c', 'l':'l',
                 'cis': 'cis', 'trans': 'trans', 's': 'syn', 'a': 'anti',
                 'Δ': 'Delta', 'Λ': 'Lambda',
                 'α': 'alpha', 'β': 'beta', 'γ': 'gamma',
                 'n': 'n', 'i': 'i', 't': 't', 'neo': 'neo', 'sec': 'sec',
                 'o': 'o', 'm': 'm', 'p': 'p', 
                 'ortho': 'ortho', 'meta': 'meta', 'para': 'para',}
# The LaTeX equivalents of these prefix tokens.
latex_prefix_dict = {'(±)': r'\pm',  'Δ': r'\Delta', 'Λ': r'\Lambda',
                     'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma'}

# also allow a comma-separated list of integers, e.g. 1,1,2-
prefix_parser = pp.delimitedList(pp.OneOrMore(integer), combine=True)
keys_list = list(prefix_tokens.keys())
for pt in keys_list:
    prefix_parser |= pp.Keyword(pt)
# Any number of prefix tokens may appear, separated by a hyphen
prefix_list_parser = (pp.delimitedList(prefix_parser, delim='-')
                       + pp.Suppress(pp.Literal('-'))).setResultsName('prefix')

# Finally, a complexChemicalFormula is a prefix, followed by one or more
# chemical_formula_fragments.
complexChemicalFormula = pp.Optional(prefix_list_parser)\
                 + chemical_formula_fragments + charge + pp.StringEnd()
# replace '+' and '-' with 'p' and 'm' to make slugs for e.g. URLs.
slug_charge_sign = {'+': 'p', '-': 'm'}

# Some Exceptions
class FormulaError(Exception):
    pass

class FormulaParseError(FormulaError):
    pass

class Formula:
    """
    A class representing a chemical formula, with methods for parsing and
    transforming its appearance as text or HTML.

    """

    def __init__(self, formula):
        """
        Initialize the Formula object by parsing the string argument
        formula.

        """

        self.formula = formula
        self.parse_formula(formula)

    def _make_prefix_html(self, prefix_list):
        """Make the prefix HTML:
            D- and L- prefixes get written in small caps
        """
        prefix = '-'.join(prefix_list)
        prefix = prefix.replace('D', '<span style="font-size: 80%;">D</span>')
        prefix = prefix.replace('L', '<span style="font-size: 80%;">L</span>')
        return '%s-' % prefix

    def _make_prefix_latex(self, prefix_list):
        """Make the prefix LaTeX."""
        latex_prefixes = []
        for prefix in prefix_list:
            try:
                latex_prefix = latex_prefix_dict[prefix]
            except KeyError:
                latex_prefix = prefix
        prefix = '-'.join(latex_prefix)
        return '{}-'.format(prefix)

    def _make_prefix_slug(self, prefix_list):
        """
        Make the prefix slug: commas are replaced by underscores and non-ASCII
        characters swapped out according to the entries in the prefix_tokens
        dictionary. For example,
            1,1,3- -> 1_1_3-
            (±)- -> pm-
            (α)- -> alpha-
        """
        slug_prefix_tokens = []
        for prefix_token in prefix_list:
            # TODO don't allow matches including numbers with leading zeros
            if re.match(r'^\d+(,\d+)*$', prefix_token):
                # this prefix token is a comma-separated list of numbers
                slug_prefix_token = prefix_token.replace(',', '_')
            else:
                # select the slug version of this prefix from prefix_tokens
                try:
                    slug_prefix_token = prefix_tokens[prefix_token]
                except KeyError:
                    raise FormulaParseError('Unrecognised formula prefix'
                                ' token: {}'.format(prefix_token))
            slug_prefix_tokens.append(slug_prefix_token)
        slug_prefix = '_'.join(slug_prefix_tokens)
        return '{}__'.format(slug_prefix)

    def parse_formula(self, formula):
        """Parse the string formula into a Formula object."""

        self.atoms = set()

        # We make a particular exception for various special cases, including
        # photons, electrons, positrons and "M", denoting an unspecified
        # "third-body" in many reactions. Note that M does not have a defined
        # charge or mass.
        if formula in special_cases:
            for attr, val in special_cases[formula].items():
                setattr(self, attr, val)
            return

        try:
            moieties = complexChemicalFormula.parseString(formula)
        except pp.ParseException:
            raise FormulaParseError('Invalid formula syntax: %s' % formula)

        self.atom_stoich = defaultdict(int)
        self.charge = 0
        self.natoms = 0
        html_chunks = []
        latex_chunks = []
        slug_chunks = []
        # calculate relative molecular mass as the sum of the atomic weights
        self.rmm = 0.

        # make the prefix html and slug
        if 'prefix' in moieties.keys():
            html_chunks.append(self._make_prefix_html(moieties['prefix']))
            latex_chunks.append(self._make_prefix_latex(moieties['prefix']))
            slug_chunks.append(self._make_prefix_slug(moieties['prefix']))

        moieties, total_charge = moieties['formula'], int(moieties['charge'])
        nmoieties = len(moieties)
        for i, moiety in enumerate(moieties):
            if 'prestoich' in moiety.keys():
                # bracketed fragment, e.g. (OH)2, 3(HO2+), ...
                prestoich = int(moiety['prestoich'])
                if prestoich > 1:
                    slug_chunks.append(moiety['prestoich'])
                    html_chunks.append(moiety['prestoich'])
                    latex_chunks.append(moiety['prestoich'])
                html_chunks.append('(')
                latex_chunks.append('(')
                slug_chunks.append('_l_')
                poststoich = int(moiety['poststoich'])
                stoich = prestoich * poststoich
            else:
                # unbracketed fragment, e.g. H2O, 2NH3, ...
                stoich = int(moiety['stoich'])
                if stoich > 1:
                    slug_chunks.append(moiety['stoich'])
                    html_chunks.append(moiety['stoich'])
                    latex_chunks.append(moiety['stoich'])
            charge = int(moiety['charge'])
            self.charge += charge * stoich
            for atom in moiety['atoms']:
                atom_symbol, atom_stoich = atom

                if atom_symbol == 'D':
                    atom_symbol = isotope.parseString('(2H)')[0]
                if atom_symbol == 'T':
                    atom_symbol = isotope.parseString('(3H)')[0]
                if isinstance(atom_symbol, pp.ParseResults):
                    # we got an isotope in the form '(zSy)' with z the mass
                    # number so symbol is the ParseResults ['z', 'Sy']:
                    mass_number, atom_symbol = (int(atom_symbol[0]),
                                                atom_symbol[1])
                    symbol_html = '<sup>%d</sup>%s' % (mass_number,atom_symbol)
                    symbol_latex = '^{{{0:d}}}\mathrm{{{1:s}}}'.format(
                                                mass_number, atom_symbol)
                    atom_symbol = '%d%s' % (mass_number, atom_symbol)
                    slug_chunks.append('-%s' % atom_symbol)
                else:
                    mass_number = None
                    symbol_html = atom_symbol
                    symbol_latex = '\\mathrm{{{0:s}}}'.format(atom_symbol)
                    slug_chunks.append(atom_symbol)

                if mass_number is not None:
                    # We have an isotope, specified as '(zSy)'.
                    try:
                        atom = isotopes[atom_symbol]
                    except KeyError:
                        raise FormulaParseError('Unknown isotope symbol'
                           ' {} in formula {}'.format(atom_symbol, formula))
                else:
                    # A regular element symbol for an atom.
                    try:
                        atom = atoms[atom_symbol]
                    except KeyError:
                        raise FormulaParseError('Unknown element symbol'
                           ' {} in formula {}'.format(atom_symbol, formula))

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
                    self.atom_stoich[atom_symbol] = None

                html_chunks.append(symbol_html)
                latex_chunks.append(symbol_latex)
                if atom_stoich != '1':
                    html_chunks.append('<sub>{}</sub>'.format(atom_stoich))
                    latex_chunks.append('_{{{0}}}'.format(atom_stoich))
                    slug_chunks.append(str(atom_stoich))

            (moiety_charge_html, moiety_charge_latex,
                         moiety_charge_slug) = self._get_charge_reps(charge)
            html_chunks.append(moiety_charge_html)
            latex_chunks.append(moiety_charge_latex)
            slug_chunks.append(moiety_charge_slug)
            #if i < nmoieties-1 and nmoieties != 1:
            #    slug_chunks.append('_d_')

            if 'poststoich' in moiety.keys():
                html_chunks.append(')')
                latex_chunks.append(')')
                slug_chunks.append('_r_')
                #if i == nmoieties and nmoieties != 1:
                #    slug_chunks.append('_d_')
                if poststoich > 1:
                    html_chunks.append('<sub>{:d}</sub>'.format(poststoich))
                    latex_chunks.append('_{{{0:d}}}'.format(poststoich))
                    slug_chunks.append('{:d}'.format(poststoich))

            if 'radical' in moiety.keys():
                html_chunks.append('&#183;')
                latex_chunks.append(r'\cdot')
                slug_chunks.append('_dot')
            if i != nmoieties - 1:
                slug_chunks.append('-')

        if total_charge:
            # TODO Refactor and test further
            self.charge = int(total_charge)
            (moiety_charge_html, moiety_charge_latex,
                       moiety_charge_slug) = self._get_charge_reps(self.charge)
            html_chunks.append(moiety_charge_html)
            latex_chunks.append(moiety_charge_latex)
            slug_chunks.append(moiety_charge_slug)

        self.html = ''.join(html_chunks)
        self.latex = ''.join(latex_chunks)
        # strip the leading '-' if the formula began with an isotope
        self.slug = ''.join(slug_chunks).lstrip('-')

        self.mass = self.rmm

    def _get_charge_reps(self, charge):
        if charge:
            s_charge = ''
            if abs(charge) > 1:
                s_charge = str(abs(charge))
            s_charge_sign = '+'
            if charge < 0:
                s_charge_sign = '-'
            moiety_charge_html = '<sup>{:s}{:s}</sup>'.format(s_charge,
                                                              s_charge_sign)
            moiety_charge_latex = '^{{{0:s}{1:s}}}'.format(s_charge,
                                                           s_charge_sign)
            moiety_charge_slug = '_{:s}{:s}'.format(
                                slug_charge_sign[s_charge_sign], s_charge)
            return moiety_charge_html, moiety_charge_latex, moiety_charge_slug
        return '', '', ''
                
    def __repr__(self):
        return self.formula
    __str__ = __repr__

    def __eq__(self, other):
        return self.formula == other.formula

    def _stoichiometric_formula_atomic_number(self):
        """Return a list of atoms/isotopes and their stoichiometries.

        The returned list is sorted in order of increasing atomic number.

        """

        atom_strs = []
        for atom in sorted(self.atoms, key=lambda e: (e.Z, e.mass)):
            if atom.is_isotope:
                symbol = '({})'.format(atom.symbol)
            else:
                symbol = atom.symbol
            atom_strs.append(self._get_symbol_stoich(symbol,
                            self.atom_stoich[atom.symbol]))
        return atom_strs

    def _stoichiometric_formula_alphabetical(self):
        """Return a list of atoms/isotopes and their stoichiometries.

        The returned list is sorted in alphabetical order.

        """

        atom_strs = self._stoichiometric_formula_atomic_number()
        atom_strs.sort()
        return atom_strs

    def stoichiometric_formula(self, fmt='atomic number'):
        """
        Return a string representation of the stoichiometric formula
        in one of the formats specified by the fmt argument:
        "atomic number": order atoms by increasing atomic number
        "alphabetical" : order atoms in alphabetical order of atomic symbol

        """

        if self.formula == 'M':
            # Special case for generic "third-body"
            return 'M'
        if self.formula == 'e-':
            # Special case for the electron
            return 'e-'
        if self.formula in ('hv', 'hν'):
            # Special case for the photon
            return 'hν'

        fmt = fmt.lower()
        if fmt not in ('atomic number', 'alphabetical'):
            raise FormulaError('Unsupported format for stoichiometric'
                    ' formula output: {}'.format(fmt))

        if fmt == 'atomic number':
            atom_strs = self._stoichiometric_formula_atomic_number()
        elif fmt == 'alphabetical':
            atom_strs = self._stoichiometric_formula_alphabetical()

        # finally, add on the charge string, e.g. '', '-', '+2', ...
        atom_strs.append(self._get_charge_string())
        return ''.join(atom_strs)

    def _get_symbol_stoich(self, symbol, stoich):
        """
        Return Xn for element symbol X and stoichiometry n, unless n is 1,
        in which case, just return X.

        """
        if stoich is None:
            return '{}x'.format(symbol)
        if stoich > 1:
            return '{}{:d}'.format(symbol, stoich)
        return symbol

    def _get_charge_string(self):
        """
        Return the string representation of the charge: '+', '-', '+2', '-3',
        etc.

        """

        if not self.charge:
            return ''
        if self.charge > 0:
            if self.charge  > 1:
                return '+{:d}'.format(self.charge)
            return '+'
        if self.charge == -1:
            return '-'
        return str(self.charge)
