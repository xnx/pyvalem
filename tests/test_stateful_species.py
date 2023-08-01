"""
Unit tests for the stateful_species module of PyValem
"""

import unittest

from pyvalem.formula import FormulaParseError
from pyvalem.states._base_state import StateParseError
from pyvalem.stateful_species import StatefulSpecies, StatefulSpeciesError
from pyvalem.states.vibrational_state import VibrationalState


class StatefulSpeciesTest(unittest.TestCase):
    def test_stateful_species_parsing(self):
        _ = StatefulSpecies("Ar *")
        _ = StatefulSpecies("Fe e5G")
        _ = StatefulSpecies("CrH 1sigma2.2sigma1.1pi4.3sigma1; 6SIGMA+")
        _ = StatefulSpecies("H(35Cl) J=2")
        _ = StatefulSpecies("OH X(2Π_1/2, J=2")

        _ = StatefulSpecies("HCl v=2 J=0")
        _ = StatefulSpecies("C2H3Cl")
        _ = StatefulSpecies("C2H2 v2+v1 J=10;X(1SIGMA+u)")
        _ = StatefulSpecies("CO *")

        ss1 = StatefulSpecies("NCO v2+3v1;J=10.5;a(2Σ-g)")
        self.assertEqual(repr(ss1.states[0]), repr(VibrationalState("ν2+3ν1")))

        self.assertRaises(StateParseError, StatefulSpecies, "C2H4 v")
        self.assertRaises(FormulaParseError, StatefulSpecies, "")

        _ = StatefulSpecies("Ne+ 1s2.2s2.2p5")
        _ = StatefulSpecies("Ne+ 1s2.2s2.2p5; 2P_3/2")
        _ = StatefulSpecies("H2- 1sigmag2.1sigmau1")

        ss2 = StatefulSpecies("H+")
        self.assertEqual(ss2.formula.charge, 1)

        # ss3 = StatefulSpecies('H+ lambda=210nm')
        # self.assertEqual(ss3.formula.charge, 1)

        _ = StatefulSpecies("CO2 2v2; l=2")

        ss4 = StatefulSpecies("Ne 3p'[3/2]_1")
        self.assertEqual(ss4.states[0].html, "3p'[3/2]<sub>1</sub>")

    def test_stateful_species_equality(self):
        ss1 = StatefulSpecies("HCl v=2;J=0")
        ss2 = StatefulSpecies("HCl J=0;v=2")

        self.assertEqual(ss1, ss2)

    def test_state_appears_at_most_once(self):
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "HCl v=0;v=1")
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "H 1s1;2s1")
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "H2 1sigma1;2sigma1")
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "CO J=0; J=1")
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "CO X(1PIu);2Σ-")
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "Ar *;**")
        self.assertRaises(StatefulSpeciesError, StatefulSpecies, "Ar 2S, 2P_3/2")
        # StatefulSpecies('CH3Cl J=2;Ka=1;Kc=2')

    def test_atomic_configuration_verification(self):
        ss1 = StatefulSpecies("Ar+ 1s2.2s2.2p6.3s2.3p5")
        self.assertTrue(ss1.verify_atomic_configuration())
        ss1 = StatefulSpecies("Ar+ [Ne].3s2.3p5")
        self.assertTrue(ss1.verify_atomic_configuration())
        ss2 = StatefulSpecies("Ar+ 1s2.2s2.2p6.3s2.3p6")
        ss3 = StatefulSpecies("Ar+ [Ne].3s2.3p6")
        ss4 = StatefulSpecies("Ar+ [Ne].3s2.3p6.4s")
        for ss in (ss2, ss3, ss4):
            self.assertRaises(StatefulSpeciesError, ss.verify_atomic_configuration)

    def test_diatomic_configuration_inversion_parity(self):
        ss1 = StatefulSpecies("H2 1sigmag2; 1SIGMA+g")
        self.assertTrue(ss1.verify_diatomic_inversion_parity())
        ss2 = StatefulSpecies("H2 1sigma2")
        ss3 = StatefulSpecies("HD 1sigmag2")
        ss4 = StatefulSpecies("H2 1sigma1.2sigmau1")
        for ss in (ss2, ss3, ss4):
            self.assertRaises(StatefulSpeciesError, ss.verify_diatomic_inversion_parity)

    def test_multiple_key_value_pair_states(self):
        _ = StatefulSpecies("Ar+ n=2;2P;|M|=1")

        ss2 = StatefulSpecies("Ar+ n=2;n=3")
        self.assertRaises(StatefulSpeciesError, ss2.verify_multiple_key_value_pairs)

    def test_stateful_species_repr(self):
        ss1 = StatefulSpecies("C2H2 v2+v1;J=10;X(1SIGMA+u)")
        self.assertTrue(repr(ss1) == "C2H2 X(1Σ+u);ν1+ν2;J=10")

        ss2 = StatefulSpecies("(235U) l=0;***;n=1")
        ss3 = StatefulSpecies("(235U) l=0;n=1;***")
        self.assertEqual(repr(ss2), repr(ss3))
        self.assertEqual(repr(ss2), "(235U) 3*;n=1;l=0")

        for ss_text in ["C+ 4P;2s2.2p1", "C+ 2s2.2p1;4P"]:
            self.assertEqual(repr(StatefulSpecies(ss_text)), "C+ 2s2.2p;4P")

        for ss_text in ["C+ 2P;2s2.2p1", "C+ 2s2.2p1;2P"]:
            self.assertEqual(repr(StatefulSpecies(ss_text)), "C+ 2s2.2p;2P")

    def test_stateful_species_key_value_pair_ordering(self):
        ss1 = StatefulSpecies("H n=3;l=1")
        self.assertEqual(repr(ss1), "H n=3;l=1")

    def test_atomic_term_symbols(self):
        ss1 = StatefulSpecies("Fe+ a3D")
        self.assertEqual(ss1.states[0].moore_label, "a")
        self.assertEqual(ss1.states[0].S, 1)

        self.assertRaises(StateParseError, StatefulSpecies, "Ti +2 A5D")


if __name__ == "__main__":
    unittest.main()
