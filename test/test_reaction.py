"""
# Unit tests for the reaction module of PyValem
"""

import unittest

from pyvalem.reaction import (Reaction, ReactionParseError,
                              ReactionStoichiometryError, ReactionChargeError)
from pyvalem.vibrational_state import VibrationalState
from pyvalem.stateful_species import StatefulSpecies


class ReactionParseTest(unittest.TestCase):

    def test_reaction_parsing(self):
        s_r1 = 'CO + O2 → CO2 + O'
        r1 = Reaction(s_r1)
        self.assertEqual(str(r1), s_r1)
        r2 = Reaction('CO v=1 + O2 J=2;X(3SIGMA-g) → CO2 + O')
        self.assertEqual(str(r2), 'CO v=1 + O2 J=2;X(3Σ-g) → CO2 + O')
        self.assertRaises(ReactionParseError, Reaction, 'CO + O2 CO2 + O')
        self.assertRaises(ReactionParseError, Reaction, 'CO + O2 = + CO2 + O')
        self.assertRaises(ReactionParseError, Reaction, 'BeH+ + I2 =⇌ BeI')
        self.assertRaises(ReactionStoichiometryError, Reaction,
                                                    'BeH + I2 ⇌ BeI')
        self.assertRaises(ReactionChargeError, Reaction,'BeH+ + I2 ⇌ BeI + HI')
        self.assertEqual(r1.reactants[0][1].__repr__(), 'CO')
        self.assertEqual(r2.reactants[0][1].states[0].__repr__(), 'v=1')
        self.assertEqual(r2.reactants[1][1].states[1].__repr__(), 'X(3Σ-g)')
        self.assertEqual(r2.html, 'CO v=1 + O<sub>2</sub> J=2;'
            ' X(<sup>3</sup>Σ<sup>-</sup><sub>g</sub>) → CO<sub>2</sub> + O')
        self.assertEqual(r2.latex, r'\mathrm{C}\mathrm{O} \; v=1 + '
                r'\mathrm{O}_{2} \; J=2; \; X({}^{3}\Sigma^-_{g}) \rightarrow '
                r'\mathrm{C}\mathrm{O}_{2} + \mathrm{O}')

        s_r3 = 'C6H5OH + 7O2 -> 6CO2 + 3H2O'
        r3 = Reaction(s_r3)
        self.assertEqual(str(r3), 'C6H5OH + 7O2 → 6CO2 + 3H2O')
        self.assertEqual(r3.latex, r'\mathrm{C}_{6}\mathrm{H}_{5}\mathrm{O}'
                r'\mathrm{H} + 7\mathrm{O}_{2} \rightarrow 6\mathrm{C}'
                r'\mathrm{O}_{2} + 3\mathrm{H}_{2}\mathrm{O}')


        s_r4 = '7O2 + C6H5OH -> 6CO2 + 3H2O'
        r4 = Reaction(s_r4)
        self.assertEqual(r3, r4)

    def test_reaction_term_aggregation(self):
        s_r1 = 'H + e- + e- -> H+ + e- + e- + e-'
        r1 = Reaction(s_r1)
        self.assertEqual(str(r1), 'H + 2e- → H+ + 3e-')

        s_r2 = 'H2 X(2PIu);v=2 + Ar + Ar → H2 a(3SIGMA-g);v=5 + Ar + Ar *'
        r2 = Reaction(s_r2)
        self.assertEqual(len(r2.reactants), 2)
        self.assertEqual(len(r2.products), 3)

    def test_reaction_equality(self):
        s_r1 = 'CO + O2 → CO2 + O'
        r1 = Reaction(s_r1)
        s_r2 = 'CO + O2 ⇌ O + CO2'
        r2 = Reaction(s_r2)
        s_r3 = 'CO + O2 → CO3'
        r3 = Reaction(s_r3)

        self.assertEqual(r1, r2)
        self.assertEqual(r1 == r3, False)

if __name__ == '__main__':
    unittest.main()


