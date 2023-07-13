"""
Unit tests for the atomic_configurations module of PyValem
"""

import unittest

from pyvalem.states.atomic_configuration import (
    AtomicConfiguration,
    AtomicConfigurationError,
)


class AtomicConfigurationTest(unittest.TestCase):
    def test_atomic_configuration(self):
        c0 = AtomicConfiguration("1s2")
        c1 = AtomicConfiguration("1s2.2s2")
        c2 = AtomicConfiguration("1s2.2s2.2p6")
        c3 = AtomicConfiguration("1s2.2s2.2p6.3s2.3d10")
        c4 = AtomicConfiguration("[He].2s1")
        c5 = AtomicConfiguration("2s2.2p1.3s")

        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "s4.w2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s 2.2s2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2. 2s2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2 2s2 2p6")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "He.2s1")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "[Bi].2s1")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1ss2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2..2s2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2,2s2,2p6")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2;2s2:2p6")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, ".1s2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "[He].[Ne]")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "[He]2s1")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2.2s2.2s1")

        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2.1s2.2s2")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2.2s2.2p7")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "1s2.2s2.2d2")

    def test_atomic_configuration_html_and_latex(self):
        c0 = AtomicConfiguration("1s2")
        c1 = AtomicConfiguration("1s2.2s2")
        c2 = AtomicConfiguration("[Ar].4s2.3d10.4p5")

        self.assertEqual(c0.html, "1s<sup>2</sup>")
        self.assertEqual(c1.html, "1s<sup>2</sup>2s<sup>2</sup>")
        self.assertEqual(c2.html, "[Ar]4s<sup>2</sup>3d<sup>10</sup>4p<sup>5</sup>")

        self.assertEqual(c0.latex, "1s^{2}")
        self.assertEqual(c1.latex, "1s^{2}2s^{2}")
        self.assertEqual(c2.latex, r"\mathrm{[Ar]}4s^{2}3d^{10}4p^{5}")

    def test_atomic_configuration_equality(self):
        c1 = AtomicConfiguration("[Ar].4s2.3d10.4p5")
        c2 = AtomicConfiguration("[Ar].4s2.3d10.4p5")
        c3 = AtomicConfiguration("1s2.2s2.2p6.3s2.3p6.4s2.3d10.4p5")
        self.assertEqual(c3.state_str, "[Ar].4s2.3d10.4p5")
        self.assertEqual(c3.html, "[Ar]4s<sup>2</sup>3d<sup>10</sup>4p<sup>5</sup>")
        c4 = AtomicConfiguration("[Ar].4s2.3d10.4p6")
        self.assertEqual(c1, c2)
        self.assertEqual(c1, c3)
        self.assertNotEqual(c1, c4)

        c5 = AtomicConfiguration("[Ne].3s")
        self.assertEqual(repr(c5), "1s2.2s2.2p6.3s")
        self.assertEqual(c5.state_str, "[Ne].3s")
        self.assertEqual(c5.html, "[Ne]3s")

        c6 = AtomicConfiguration("1s2.2s2.2p6")
        self.assertEqual(repr(c6), "1s2.2s2.2p6")
        self.assertEqual(c6.state_str, "1s2.2s2.2p6")

        c7 = AtomicConfiguration("1s2.2s2.2p6.3s2.3p6.3d10.4s2.4p6.4d10.5s2.5p6.5d1")
        self.assertEqual(repr(c7), "1s2.2s2.2p6.3s2.3p6.3d10.4s2.4p6.4d10.5s2.5p6.5d")
        self.assertEqual(c7.state_str, "[Xe].5d1")
        self.assertEqual(c7.html, "[Xe]5d")

    def test_excited_atomic_configuration(self):
        c1 = AtomicConfiguration("5g1")
        self.assertRaises(AtomicConfigurationError, AtomicConfiguration, "4g1")
        c2 = AtomicConfiguration("10k1")
        c3 = AtomicConfiguration("1s2.2s2.2p5.7h2")

    def test_atomic_configuration_repr(self):
        c1 = AtomicConfiguration("1s2.2s2.2p6.3s2.3p6.4s2.3d")
        c2 = AtomicConfiguration("[Ar].4s2.3d1")
        self.assertEqual(repr(c1), "1s2.2s2.2p6.3s2.3p6.4s2.3d")
        self.assertEqual(repr(c2), "1s2.2s2.2p6.3s2.3p6.4s2.3d")

    def test_atomic_configuration_default_nocc(self):
        c1 = AtomicConfiguration("1s")
        self.assertEqual(c1.nelectrons, 1)
        self.assertEqual(c1.orbitals[0].nocc, 1)
        c2 = AtomicConfiguration("1s2.2s")
        self.assertEqual(c2.nelectrons, 3)
        self.assertEqual(c2.orbitals[0].nocc, 2)
        self.assertEqual(c2.orbitals[1].nocc, 1)
        c3 = AtomicConfiguration("1s1.2s2")
        self.assertEqual(c3.nelectrons, 3)
        self.assertEqual(c3.orbitals[0].nocc, 1)
        self.assertEqual(c3.orbitals[1].nocc, 2)


if __name__ == "__main__":
    unittest.main()
