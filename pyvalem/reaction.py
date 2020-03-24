import re
from .stateful_species import StatefulSpecies
from .formula import FormulaParseError

class ReactionParseError(Exception):
    pass

class ReactionStoichiometryError(ReactionParseError):
    pass

class ReactionChargeError(ReactionParseError):
    pass

class Reaction:

    RP_SEPARATORS = ' → ', ' = ', ' ⇌ ', ' -> ', ' <-> ', ' <=> '

    canonical_separators = {'→': '→', '->': '→', '=': '→',
                            '⇌': '⇌', '<->': '⇌', '<=>': '⇌'}
    latex_sep = {'→': r'\rightarrow', '⇌': r'\rightlefthooks'}

    def __init__(self, s):

        for sep in Reaction.RP_SEPARATORS:
            fragments = s.split(sep)
            nfragments = len(fragments)
            if nfragments == 1:
                continue
            if nfragments > 2:
                raise ReactionParseError('Invalid reaction string'
                        ' - multiple reactant-product separators: {}'.format(s))
            break
        else:
            raise ReactionParseError('Invalid reaction string'
                        ' - no reactant-product separator: {}'.format(s))
        self.sep = Reaction.canonical_separators[sep.strip()]

        reactants, products = [f.split(' + ') for f in fragments]
        try:
            self.reactants = [self._parse_ss_with_stoich_coeff(s) for s in
                              reactants]
            self.products = [self._parse_ss_with_stoich_coeff(s) for s in
                              products]
        except FormulaParseError as err:
             raise ReactionParseError('Failed to parse Reaction string "{}"'
                ' because one of the StatefulSpecies was incorrectly formed.'
                ' The error reported was: {}'.format(s, err))

        self.reactants = self._aggregate_terms(self.reactants)
        self.products = self._aggregate_terms(self.products)

        if not self.stoichiometry_conserved():
            raise ReactionStoichiometryError('Stoichiometry not preserved for'
                    ' reaction: {}'.format(s))
        if not self.charge_conserved():
            raise ReactionChargeError('Charge not preserved for'
                    ' reaction: {}'.format(s))

        self._order_terms(self.reactants)
        self._order_terms(self.products)


    def _aggregate_terms(self, terms):
        """
        Collect separate terms involving the same StatefulSpecies into a single
        term with the same total stoichiometry. e.g. H + e + e becomes H + 2e.

        """

        ss_set = set(term[1] for term in terms)
        aggregated_terms = []
        for ss in ss_set:
            n = sum(st[0] for st in terms if st[1] == ss)
            aggregated_terms.append((n, ss))
        return aggregated_terms

    def _order_terms(self, terms):
        """
        Sort the reactant or product terms alphabetically by formula first,
        then stoichiometry.

        """

        terms.sort(key=lambda e: (e[1].formula.formula, e[0]))

    def _parse_ss_with_stoich_coeff(self, s):
        """
        Parse s into n<ss> where n is a stoichiometric coefficient and ss
        a StatefulSpecies.

        """

        patt = '(\d*)(.*)'
        n, ss = re.match(patt, s).groups()
        if not n:
            n = 1
        else:
            try:
                n = int(n)
            except ValueError:
                raise ReactionParseError('Failed to parse {}'.format(s))
        ss = StatefulSpecies(ss)
        return n, ss

    def __repr__(self):
        reactants = ' + '.join([self._get_str_term(n, r)
                                    for n, r in self.reactants])
        products = ' + '.join([self._get_str_term(n, p)
                                    for n, p in self.products])
        return '{} {} {}'.format(reactants, self.sep, products)
    __str__ = __repr__

    def _get_str_term(self, n, term):
        s_n = str(n) if n != 1 else ''
        return '{}{}'.format(s_n, term)


    def _get_all_stoichs(self, ss_list):
        stoich = {}
        for n, ss in ss_list:
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

        if reactants_stoich == products_stoich:
            return True
        return False


    def _get_total_charge(self, ss_list):
        return sum(n * ss.formula.charge for n,ss in ss_list)


    def charge_conserved(self):
        """Verify that the Reaction object conserves charge."""

        reactants_total_charge = self._get_total_charge(self.reactants)
        products_total_charge = self._get_total_charge(self.products)

        if reactants_total_charge == products_total_charge:
            return True
        return False

    def __eq__(self, other):
        return (set(self.reactants) == set(other.reactants) and
                set(self.products) == set(other.products))

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def html(self):
        def _rp_html(n, rp):
            if n == 1:
                n = ''
            return '{}{}'.format(n, rp.html)

        reactant_html_chunks = []
        for n, reactant in self.reactants:
            reactant_html_chunks.append(_rp_html(n, reactant))
        html_chunks = [' + '.join(reactant_html_chunks)]
        html_chunks.append(' {} '.format(self.sep))
        product_html_chunks = []
        for n, product in self.products:
            product_html_chunks.append(_rp_html(n, product))
        html_chunks.append(' + '.join(product_html_chunks))
        return ''.join(html_chunks)

    @property
    def latex(self):
        def _rp_latex(n, rp):
            if n == 1:
                n = ''
            return '{}{}'.format(n, rp.latex)

        reactant_latex_chunks = []
        for n, reactant in self.reactants:
            reactant_latex_chunks.append(_rp_latex(n, reactant))
        latex_chunks = [' + '.join(reactant_latex_chunks)]
        latex_chunks.append(' {} '.format(Reaction.latex_sep[self.sep]))
        product_latex_chunks = []
        for n, product in self.products:
            product_latex_chunks.append(_rp_latex(n, product))
        latex_chunks.append(' + '.join(product_latex_chunks))
        return ''.join(latex_chunks)
