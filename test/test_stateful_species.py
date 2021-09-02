"""
Unit tests for the stateful_species module of PyValem
"""

import unittest

from pyvalem.state import StateParseError
from pyvalem.vibrational_state import VibrationalState
from pyvalem.stateful_species import StatefulSpecies, StatefulSpeciesError
from pyvalem.formula import FormulaParseError


class StatefulSpeciesTest(unittest.TestCase):

    def test_stateful_species_parsing(self):

        ss = StatefulSpecies('Ar *')
        ss = StatefulSpecies('CrH 1sigma2.2sigma1.1pi4.3sigma1; 6SIGMA+')
        ss = StatefulSpecies('H(35Cl) J=2')
        ss = StatefulSpecies('OH X(2Π_1/2; J=2')

        ss1 = StatefulSpecies('HCl v=2;J=0')
        ss2 = StatefulSpecies('C2H3Cl')
        ss3 = StatefulSpecies('C2H2 v2+v1;J=10;X(1SIGMA+u)')
        ss4 = StatefulSpecies('NCO v2+3v1;J=10.5;a(2Σ-g)')
        ss5 = StatefulSpecies('CO *')
        self.assertRaises(StateParseError, StatefulSpecies, 'C2H4 v')
        self.assertRaises(FormulaParseError, StatefulSpecies, '')
        self.assertEqual(repr(ss4.states[0]), repr(VibrationalState('ν2+3ν1')))

        ss = StatefulSpecies('Ne+ 1s2.2s2.2p5')
        ss = StatefulSpecies('Ne+ 1s2.2s2.2p5; 2P_3/2')
        ss = StatefulSpecies('H2- 1sigmag2.1sigmau1')

        ss6 = StatefulSpecies('H+')
        self.assertEqual(ss6.formula.charge, 1)

#        ss7 = StatefulSpecies('H+ lambda=210nm')
#        self.assertEqual(ss7.formula.charge, 1)

        ss8 = StatefulSpecies('CO2 2v2; l=2')

        ss9 = StatefulSpecies("Ne 3p'[3/2]_1")
        self.assertEqual(ss9.states[0].html, "3p'[3/2]<sub>1</sub>")

    def test_stateful_species_equality(self):

        ss1 = StatefulSpecies('HCl v=2;J=0')
        ss2 = StatefulSpecies('HCl J=0;v=2')

        self.assertEqual(ss1, ss2)

    def test_state_appears_at_most_once(self):
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, 'HCl v=0;v=1')
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, 'H 1s1;2s1')
        self.assertRaises(StatefulSpeciesError, StatefulSpecies,
                    'H2 1sigma1;2sigma1')
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, 'CO J=0;J=1')
        self.assertRaises(StatefulSpeciesError, StatefulSpecies,
                    'CO X(1PIu);2Σ-')
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, 'Ar *;**')
        self.assertRaises(StatefulSpeciesError, StatefulSpecies,
                    'Ar 2S;2P_3/2')

#        StatefulSpecies('CH3Cl J=2;Ka=1;Kc=2')

    def test_atomic_configuration_verification(self):
        ss1 = StatefulSpecies('Ar+ 1s2.2s2.2p6.3s2.3p5')
        self.assertTrue(ss1.verify_atomic_configuration())
        ss1 = StatefulSpecies('Ar+ [Ne].3s2.3p5')
        self.assertTrue(ss1.verify_atomic_configuration())
        ss2 = StatefulSpecies('Ar+ 1s2.2s2.2p6.3s2.3p6')
        ss3 = StatefulSpecies('Ar+ [Ne].3s2.3p6')
        ss4 = StatefulSpecies('Ar+ [Ne].3s2.3p6.4s1')
        for ss in (ss2, ss3, ss4):
            self.assertRaises(StatefulSpeciesError,
                              ss.verify_atomic_configuration)

    def test_diatomic_configuration_inversion_parity(self):
        ss1 = StatefulSpecies('H2 1sigmag2; 1SIGMA+g')
        self.assertTrue(ss1.verify_diatomic_inversion_parity())
        ss2 = StatefulSpecies('H2 1sigma2')
        ss3 = StatefulSpecies('HD 1sigmag2')
        ss4 = StatefulSpecies('H2 1sigma1.2sigmau1')
        for ss in (ss2, ss3, ss4):
            self.assertRaises(StatefulSpeciesError,
                              ss.verify_diatomic_inversion_parity)


    def test_multiple_key_value_pair_states(self):
        ss1 = StatefulSpecies('Ar+ n=2;2P;|M|=1')

        ss2 = StatefulSpecies('Ar+ n=2;n=3')
        self.assertRaises(StatefulSpeciesError,
                          ss2.verify_multiple_key_value_pairs)


    def test_stateful_species_repr(self):
        ss1 = StatefulSpecies('C2H2 v2+v1;J=10;X(1SIGMA+u)')
        self.assertTrue(repr(ss1) == 'C2H2 J=10;X(1Σ+u);ν1+ν2')

if __name__ == '__main__':
    unittest.main()

