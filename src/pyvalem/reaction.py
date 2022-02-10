"""
This module contains the `Reaction` class representing a chemical process.

A reaction consists of one or more reactants and one or more products, all being
instances of the `StatefulSpecies` class (with or without states.).
A `Reaction` is instantiated by passing an ``r_str`` argument, a pyvalem-compatible
reaction string.

As with other pyvalem objects, the ``__repr__`` method is overloaded to provide a
*canonicalised* representation of the `Reaction` instance.

Examples
--------
>>> from pyvalem.reaction import Reaction
>>> Reaction('CO v=1 + O2 J=2;X(3SIGMA-g) → CO2 + O')
CO v=1 + O2 X(3Σ-g);J=2 → CO2 + O

>>> Reaction('CO + O2 <-> CO2 + O')
CO + O2 ⇌ CO2 + O

>>> Reaction('HCl + hv -> H+ + Cl + e-')
hν + HCl → H+ + Cl + e-

>>> str(Reaction('C6H5OH + 7O2 → 6CO2 + 3H2O'))
'C6H5OH + 7O2 → 6CO2 + 3H2O'

>>> repr(Reaction('C6H5OH + 7O2 → 6CO2 + 3H2O'))
'C6H5OH + O2 + O2 + O2 + O2 + O2 + O2 + O2 → CO2 + CO2 + CO2 + CO2 + CO2 + CO2 + H2O + H2O + H2O'
"""

import re

from .formula import FormulaParseError
from .stateful_species import StatefulSpecies


class ReactionParseError(Exception):
    pass


class ReactionStoichiometryError(ReactionParseError):
    pass


class ReactionChargeError(ReactionParseError):
    pass


class Reaction:
    """A class representing a reaction between species.

    A `Reaction` object is a collection of reactants and products, each of which is
    represented by a `StatefulSpecies` (though an individual species need not be
    associated with a specified state).
    It is instantiated using a string consisting of reactant and product
    `StatefulSpecies` valid strings, each separated by a plus sign surrounded by
    whitespace: ``" + "``.
    Reactants and products are separated by any of the following side separator strings:
    ``' → '``, ``' = '``, ``' ⇌ '``, ``' -> '``, ``' <-> '``, ``' <=> '``.

    The `Reaction` class implements ``html`` and ``latex`` attributes to render nice
    representations.

    Parameters
    ----------
    r_str : str
        PyValem-valid reaction string, see above.
    strict : bool, default=True
        If ``strict=False``, the stoichiometry and charge balance is not enforced.
        This is intended for incomplete or ambiguous reactions.

    Attributes
    ----------
    reactants : list of tuple[int, StatefulSpecies]
        Aggregated `StatefulSpecies` instances with their stoichiometries
    products : list of tuple[int, StatefulSpecies]
        Aggregated `StatefulSpecies` instances with their stoichiometries
    html
    latex

    Raises
    ------
    ReactionStoichiometryError
        If ``strict=True`` and the elemental stoichiometry is *not conserved*.
    ReactionChargeError
        If ``strict=True`` and the reaction charge is *not conserved*.

    Notes
    -----
    The ``__repr__`` method is overloaded to provie a *canonicalised* representation
    of the reaction. The idea is that two `Reaction` instances representing the same
    physical entity will have the same ``repr(reaction)`` text representation.
    The ``repr`` canonicalises the `StatefulSpecies` representations (all the way down
    to `Formula`, `State` and the states order), the sides separator, and expands all
    aggregated species (``"2H"`` becomes ``"H + H"``), while keeping the order of all
    the heavy species as passed as ``r_str``.
    All the light species, however, are aggregated and moved to the beginning of the
    *left-hand-side* of the reaction and to the end of the *right-hand-side* of the
    reaction.

    Examples
    --------
    >>> r1 = Reaction('CO v=1 + O2 J=2;X(3SIGMA-g) → CO2 + O')
    >>> r2 = Reaction('CO + O2 <-> CO2 + O')
    >>> r3 = Reaction('HCl + hv -> H+ + Cl + e-')
    >>> r4 = Reaction('C6H5OH + 7O2 → 6CO2 + 3H2O')

    >>> # Demonstration of the canonicalisation:
    >>> str(r3)  # non-canonical string repr.
    'HCl + hν → H+ + Cl + e-'

    >>> repr(r3)  # canonicalised representation
    'hν + HCl → H+ + Cl + e-'

    >>> str(r4)  # non-canonical string repr.
    'C6H5OH + 7O2 → 6CO2 + 3H2O'

    >>> repr(r4)  # canonicalised representation
    'C6H5OH + O2 + O2 + O2 + O2 + O2 + O2 + O2 → CO2 + CO2 + CO2 + CO2 + CO2 + CO2 + H2O + H2O + H2O'

    >>> # HTML attribute
    >>> r1.html
    'CO v=1 + O<sub>2</sub> J=2 X<sup>3</sup>Σ<sup>-</sup><sub>g</sub> → CO<sub>2</sub> + O'

    >>> # Consistency checks
    >>> Reaction('BeH+ + I2 <-> BeI + HI')
    Traceback (most recent call last):
      ...
    pyvalem.reaction.ReactionChargeError: Charge not preserved for reaction: BeH+ + I2 <-> BeI + HI

    >>> Reaction('BeH + I2 <-> BeI')
    Traceback (most recent call last):
      ...
    pyvalem.reaction.ReactionStoichiometryError: Stoichiometry not preserved for reaction: BeH + I2 <-> BeI

    >>> Reaction('BeH+ + I2 <->', strict=False)
    BeH+ + I2 ⇌
    """

    RP_SEPARATORS = "→", "=", "⇌", "->", "<->", "<=>"
    SPACED_RP_SEPARATORS = [" " + s + " " for s in RP_SEPARATORS]

    canonical_separators = {
        "→": "→",
        "->": "→",
        "=": "→",
        "⇌": "⇌",
        "<->": "⇌",
        "<=>": "⇌",
    }
    latex_sep = {"→": r"\rightarrow", "⇌": r"\rightlefthooks"}

    light_species = ("e-", "e+", "hv", "hν")

    def __init__(self, r_str, strict=True):
        # If the Reaction string has no products, add a space after the
        # separator (e.g. 'Ar + e- ->' becomes 'Ar + e- -> ').
        for sep in Reaction.RP_SEPARATORS:
            if r_str.rstrip().endswith(sep):
                r_str = r_str + " "
                break

        for sep in Reaction.SPACED_RP_SEPARATORS:
            fragments = r_str.split(sep)
            # fragments is a list: [LHS_str, RHS_str]
            if len(fragments) == 1:
                continue
            elif len(fragments) > 2:
                raise ReactionParseError(
                    "Invalid reaction string - multiple reactant-product "
                    "separators: {}".format(r_str)
                )
            break
        else:
            raise ReactionParseError(
                "Invalid reaction string - no reactant-product separator: "
                "{}".format(r_str)
            )

        # canonicalised side separator:
        self.sep = self.canonical_separators[sep.strip()]

        # parse reactants and products into
        # dict[str, int]
        # and
        # list[tuple[int: stoichiometry, StatefulSpecies]]
        self.reactants_text_count_map = None
        self.products_text_count_map = None
        self.reactants = None
        self.products = None
        try:
            self._parse_species(*fragments)
        except FormulaParseError as err:
            raise ReactionParseError(
                'Failed to parse Reaction string "{}" because one of the '
                "StatefulSpecies was incorrectly formed. "
                "The error reported was: {}".format(r_str, err)
            )

        # validate charge and stoichiometry conservation:
        if strict and not self.stoichiometry_conserved():
            raise ReactionStoichiometryError(
                "Stoichiometry not preserved for " "reaction: {}".format(r_str)
            )
        if strict and not self.charge_conserved():
            raise ReactionChargeError(
                "Charge not preserved for " "reaction: {}".format(r_str)
            )

    def _parse_species(self, lhs_str, rhs_str):
        """Parse strings of both sides of the reaction string

        Parses into self.reactants and self.products in the form of lists of
        (species_count, StatefulSpecies) tuples.
        On the side, also creates maps between species string (as passed
        to the constructor) and number of species on the side.
        Those are self.reactants_text_count_map and self.products_text_count_map.

        Populates ``self.reactants``, ``self.products``,
        ``self.reactants_text_count_map``, and ``self.products_text_count_map``

        Parameters
        ----------
        lhs_str, rhs_str : str
            Strings of reactants and products sides, around the sides separator from
            the ``r_str``.
        """
        self.reactants_text_count_map = {}
        self.products_text_count_map = {}
        self.reactants = []
        self.products = []
        for side_str, species, species_map in zip(
            [lhs_str, rhs_str],
            [self.reactants, self.products],
            [self.reactants_text_count_map, self.products_text_count_map],
        ):
            for side_fragment in side_str.split(" + "):
                if side_fragment.strip():
                    patt = r"(\d*)(.*)"
                    n, ss_str = re.match(patt, side_fragment).groups()
                    if not n:
                        n = 1
                    else:
                        try:
                            n = int(n)
                        except ValueError:
                            raise ReactionParseError(
                                "Failed to parse {}".format(side_fragment)
                            )
                    ss = StatefulSpecies(ss_str)
                    species.append((n, ss))
                    ss_str = str(ss)
                    if ss_str not in species_map:
                        species_map[ss_str] = 0
                    species_map[ss_str] += n

    @staticmethod
    def _sort_terms(terms, side="lhs"):
        """Sorts the species for the canonicalised representation.

        The only sorting is performed on light species, these are placed
        first on LHS and last on RHS of the reaction.

        Parameters
        ----------
        terms : iterable of tuple[int, StatefulSpecies]
        side : {"lhs", "rhs"}, default="lhs"

        Returns
        -------
        list of tuple[int, StatefulSpecies]
        """
        sort_keys = {sp: (-1, sp) for sp in Reaction.light_species}
        return list(
            sorted(
                terms,
                key=lambda e: sort_keys.get(e[1].formula.formula, (0, "")),
                reverse=side != "lhs",
            )
        )

    def _aggregate_terms(self, terms):
        """Aggregates the same light species into a single term.

        Accepts list[tuple[int, StatefulSpecies]].
        Collect separate terms involving the same StatefulSpecies into a single
        term with the same total stoichiometry.
        The aggregation is only done on successive light species terms. This is
        connected to the canonicalisation by the ``__repr__`` method.

        Parameters
        ----------
        terms : list of tuple[int, StatefulSpecies]

        Returns
        -------
        list of tuple[int, StatefulSpecies]

        Examples
        --------
        H + H + e + e + He + e + e -> H + H + 2e + He + 2e
        """
        if not len(terms):
            return []
        aggregated_terms = [terms[0]]
        for term in terms[1:]:
            if term[1].formula.formula in self.light_species:
                last_term = aggregated_terms[-1]
                if term[1] == last_term[1]:
                    n = term[0] + last_term[0]
                    aggregated_terms[-1] = (n, term[1])
                else:
                    aggregated_terms.append(term)
            else:
                aggregated_terms.append(term)
        return aggregated_terms

    def _expand_terms(self, terms):
        """Method to expand all aggregated heavy species terms.

        Used for the canonicalised representation given by ``__repr__``.

        Parameters
        ----------
        terms : list of tuple[int, StatefulSpecies]

        Returns
        -------
        list of tuple[int, StatefulSpecies]
        """
        expanded_terms = []
        for n, ss in terms:
            if ss.formula.formula in self.light_species:
                expanded_terms.append((n, ss))
            else:
                for _ in range(n):
                    expanded_terms.append((1, ss))
        return expanded_terms

    @staticmethod
    def _silent_n(n):
        return str(n) if n != 1 else ""

    def __str__(self):
        reactants_str = " + ".join(
            "{}{}".format(self._silent_n(n), str(ss)) for n, ss in self.reactants
        )
        products_str = " + ".join(
            "{}{}".format(self._silent_n(n), str(ss)) for n, ss in self.products
        )
        return "{} {} {}".format(reactants_str, self.sep, products_str).strip()

    def __repr__(self):
        """
        Performs canonicalisation of the reaction string by expanding
        aggregated stoichiometries of all the heavy species and by aggregating
        light species (e, hv) and moving them to the side.
        """
        reactants = self._sort_terms(self.reactants, side="lhs")
        products = self._sort_terms(self.products, side="rhs")
        reactants = self._aggregate_terms(reactants)
        products = self._aggregate_terms(products)
        reactants = self._expand_terms(reactants)
        products = self._expand_terms(products)

        reactants_repr = " + ".join(
            "{}{}".format(self._silent_n(n), repr(ss)) for n, ss in reactants
        )
        products_repr = " + ".join(
            "{}{}".format(self._silent_n(n), repr(ss)) for n, ss in products
        )
        return "{} {} {}".format(reactants_repr, self.sep, products_repr).strip()

    @staticmethod
    def _get_all_stoichs(side):
        stoich = {}
        for n, ss in side:
            for sp, nn in ss.formula.atom_stoich.items():
                if sp in stoich:
                    stoich[sp] += n * nn
                else:
                    stoich[sp] = n * nn
        return stoich

    def stoichiometry_conserved(self):
        """Verify that the `Reaction` instance conserves its stoichiometry.

        Returns
        -------
        bool
        """
        reactants_stoich = self._get_all_stoichs(self.reactants)
        products_stoich = self._get_all_stoichs(self.products)

        return reactants_stoich == products_stoich

    @staticmethod
    def _get_total_charge(side):
        return sum(n * ss.formula.charge for n, ss in side if ss.formula.formula != "M")

    def charge_conserved(self):
        """Verify that the `Reaction` instance conserves its charge.

        Returns
        -------
        bool
        """
        reactants_total_charge = self._get_total_charge(self.reactants)
        products_total_charge = self._get_total_charge(self.products)

        return reactants_total_charge == products_total_charge

    def __eq__(self, other):
        return repr(self) == repr(other)

    @property
    def html(self):
        """HTML representation of the `Reaction` instance.

        Returns
        -------
        str
        """
        reactants_html = " + ".join(
            "{}{}".format(self._silent_n(n), ss.html) for n, ss in self.reactants
        )
        products_html = " + ".join(
            "{}{}".format(self._silent_n(n), ss.html) for n, ss in self.products
        )
        return "{} {} {}".format(reactants_html, self.sep, products_html).strip()

    @property
    def latex(self):
        """LaTeX representation of the `Reaction` instance.

        Returns
        -------
        str
        """
        reactants_latex = " + ".join(
            "{}{}".format(self._silent_n(n), ss.latex) for n, ss in self.reactants
        )
        products_latex = " + ".join(
            "{}{}".format(self._silent_n(n), ss.latex) for n, ss in self.products
        )
        return "{} {} {}".format(
            reactants_latex, self.latex_sep[self.sep], products_latex
        ).strip()
