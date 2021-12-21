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
        """
        Is strict flag set to False, the stoichiometry and charge balance
        is not enforced. This is intended for incomplete/ambiguous reactions.
        """
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
        """
        Parse strings of both sides of the reaction string into
        self.reactants and self.products in the form of lists of
        (species_count, StatefulSpecies).
        On the side, also creates maps between species string (as passed
        to the constructor) and number of species on the side.
        Those are self.reactants_text_count_map and
        self.products_text_count_map.
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
                    if ss_str not in species_map:
                        species_map[ss_str] = 0
                    species_map[ss_str] += n

    @staticmethod
    def _sort_terms(terms, side="lhs"):
        """
        The only sorting is performed on light species, these are placed
        first on LHS and last on RHS of the reaction.
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
        """
        Accepts list[tuple[int, StatefulSpecies]].
        Collect separate terms involving the same StatefulSpecies into a single
        term with the same total stoichiometry.
        The aggregation is only done on successive light species terms.
        Examples:
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
        """
        Method to expand all aggregated heave species terms. Used for
        the canonicalised representation given by __repr__.
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
        """Verify that the Reaction object conserves its stoichiometry."""
        reactants_stoich = self._get_all_stoichs(self.reactants)
        products_stoich = self._get_all_stoichs(self.products)

        return reactants_stoich == products_stoich

    @staticmethod
    def _get_total_charge(side):
        return sum(n * ss.formula.charge for n, ss in side if ss.formula.formula != "M")

    def charge_conserved(self):
        """Verify that the Reaction object conserves charge."""

        reactants_total_charge = self._get_total_charge(self.reactants)
        products_total_charge = self._get_total_charge(self.products)

        return reactants_total_charge == products_total_charge

    def __eq__(self, other):
        return repr(self) == repr(other)

    @property
    def html(self):
        reactants_html = " + ".join(
            "{}{}".format(self._silent_n(n), ss.html) for n, ss in self.reactants
        )
        products_html = " + ".join(
            "{}{}".format(self._silent_n(n), ss.html) for n, ss in self.products
        )
        return "{} {} {}".format(reactants_html, self.sep, products_html).strip()

    @property
    def latex(self):
        reactants_latex = " + ".join(
            "{}{}".format(self._silent_n(n), ss.latex) for n, ss in self.reactants
        )
        products_latex = " + ".join(
            "{}{}".format(self._silent_n(n), ss.latex) for n, ss in self.products
        )
        return "{} {} {}".format(
            reactants_latex, self.latex_sep[self.sep], products_latex
        ).strip()
