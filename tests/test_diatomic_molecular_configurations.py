"""
Unit tests for the diatomic molecular configuration module of PyValem
"""

import unittest

from pyvalem.states.diatomic_molecular_configuration import (
    DiatomicMolecularConfiguration,
    DiatomicMolecularConfigurationError,
)
from pyvalem.states._base_state import StateParseError


class DiatomicMolecularConfigurationTest(unittest.TestCase):
    def test_diatomic_molecular_configuration(self):
        c1 = DiatomicMolecularConfiguration("1σ")
        self.assertEqual(c1.html, "1σ<sup>1</sup>")
        self.assertEqual(c1.latex, r"1\sigma^{1}")

        c2 = DiatomicMolecularConfiguration("1σ2")
        self.assertEqual(c2.html, "1σ<sup>2</sup>")
        self.assertEqual(c2.latex, r"1\sigma^{2}")

        c3 = DiatomicMolecularConfiguration("1σg2")
        self.assertEqual(c3.html, "1σ<sub>g</sub><sup>2</sup>")
        self.assertEqual(c3.latex, r"1\sigma_g^{2}")

        c4 = DiatomicMolecularConfiguration("1σu2")
        self.assertEqual(c4.html, "1σ<sub>u</sub><sup>2</sup>")
        self.assertEqual(c4.latex, r"1\sigma_u^{2}")

        c5 = DiatomicMolecularConfiguration("1sigmau")
        self.assertEqual(str(c5), "1σu1")
        self.assertEqual(repr(c5), "1σu1")
        self.assertEqual(c5.html, "1σ<sub>u</sub><sup>1</sup>")
        self.assertEqual(c5.latex, r"1\sigma_u^{1}")

        c6 = DiatomicMolecularConfiguration("1sigmau2")
        self.assertEqual(c6.html, "1σ<sub>u</sub><sup>2</sup>")
        self.assertEqual(c6.latex, r"1\sigma_u^{2}")

        c7 = DiatomicMolecularConfiguration("1sigmau2.2sigmag1")
        self.assertEqual(
            c7.html, "1σ<sub>u</sub><sup>2</sup>.2σ<sub>g</sub>" "<sup>1</sup>"
        )
        self.assertEqual(c7.latex, r"1\sigma_u^{2}2\sigma_g^{1}")

        # N2
        c8 = DiatomicMolecularConfiguration("1σg2.1σu2.2σg2.2σu2.1πu4.3σg2")
        self.assertEqual(
            c8.latex,
            r"1\sigma_g^{2}1\sigma_u^{2}2\sigma_g^{2}"
            r"2\sigma_u^{2}1\pi_u^{4}3\sigma_g^{2}",
        )
        # NO
        c9 = DiatomicMolecularConfiguration("1σ2.2σ2.3σ2.4σ2.1π4.5σ2.2π1")
        self.assertEqual(
            c9.latex,
            r"1\sigma^{2}2\sigma^{2}3\sigma^{2}"
            r"4\sigma^{2}1\pi^{4}5\sigma^{2}2\pi^{1}",
        )

        self.assertRaises(StateParseError, DiatomicMolecularConfiguration, "s4.w2")

        self.assertRaises(
            DiatomicMolecularConfigurationError,
            DiatomicMolecularConfiguration,
            "1σu2.1σu2",
        )
        self.assertRaises(
            DiatomicMolecularConfigurationError,
            DiatomicMolecularConfiguration,
            "1σu2.1σu1",
        )
        self.assertRaises(
            DiatomicMolecularConfigurationError,
            DiatomicMolecularConfiguration,
            "1sigma3",
        )
        self.assertRaises(
            DiatomicMolecularConfigurationError, DiatomicMolecularConfiguration, "1pi6"
        )

    def test_diatomic_molecular_configuration_equality(self):
        c1 = DiatomicMolecularConfiguration("1σu2")
        c2 = DiatomicMolecularConfiguration("1sigmau2")
        c3 = DiatomicMolecularConfiguration("1sigmag2")
        self.assertEqual(c1, c2)
        self.assertNotEqual(c2, c3)

        c4 = DiatomicMolecularConfiguration("1σg2.1σu2.2σg2.2σu2.1πu4.3σg1")
        c5 = DiatomicMolecularConfiguration("1σg2.1σu2.2σg2.2σu2.1πu4.3σg1")
        self.assertEqual(c4, c5)

    def test_diatomic_molecular_configuration_repr(self):
        c1 = DiatomicMolecularConfiguration("1σu2")
        c2 = DiatomicMolecularConfiguration("1sigmau2")

        self.assertEqual(c1, c2)
        self.assertTrue(repr(c1) == repr(c2) == "1σu2")

        c3 = DiatomicMolecularConfiguration("1piu4.1pig3")
        c4 = DiatomicMolecularConfiguration("1πu4.1πg3")
        self.assertEqual(c3, c4)
        self.assertTrue(repr(c3) == repr(c4) == "1πu4.1πg3")

    def test_alt_diatomic_molecular_configuration(self):
        _ = DiatomicMolecularConfiguration("1s-σg2")
        c = DiatomicMolecularConfiguration("1s-σg2.1s-sigmau2")
        self.assertEqual(str(c), "1s-σg2.1s-σu2")
        _ = DiatomicMolecularConfiguration("1s-σ2.2p-π1")

        self.assertRaises(
            DiatomicMolecularConfigurationError,
            DiatomicMolecularConfiguration,
            "1s-σ2.1s-σ1",
        )


if __name__ == "__main__":
    unittest.main()
