"""
Unit tests for the molecular_term_symbol module of PyValem
"""

import unittest

from pyvalem.states.molecular_term_symbol import (
    MolecularTermSymbol,
    MolecularTermSymbolError,
)


class MolecularTermSymbolTest(unittest.TestCase):
    def test_molecular_term_symbol(self):
        c0 = MolecularTermSymbol("X(3Π)")
        self.assertEqual(c0.Smult, 3)
        self.assertEqual(c0.irrep, "Π")
        self.assertEqual(c0.term_label, "X")
        self.assertEqual(c0.html, "X<sup>3</sup>Π")
        self.assertEqual(c0.latex, r"X{}^{3}\Pi")

        c1 = MolecularTermSymbol('(2A")')
        self.assertEqual(c1.irrep, 'A"')
        self.assertIsNone(c1.term_label)
        self.assertEqual(c1.html, '<sup>2</sup>A"')
        self.assertEqual(c1.latex, "{}^{2}A''")

        self.assertRaises(MolecularTermSymbolError, MolecularTermSymbol, "X(Π)")

        c2 = MolecularTermSymbol("b(4Π_-3/2)")
        self.assertEqual(c2.irrep, "Π")
        self.assertEqual(c2.Smult, 4)
        self.assertEqual(c2.term_label, "b")
        self.assertEqual(c2.Omega, -1.5)
        self.assertEqual(c2.html, "b<sup>4</sup>Π<sub>-3/2</sub>")
        self.assertEqual(c2.latex, r"b{}^{4}\Pi{}_{-3/2}")

        c3 = MolecularTermSymbol("A'(1A1g_0)")
        self.assertEqual(c3.irrep, "A1g")
        self.assertEqual(c3.Smult, 1)
        self.assertEqual(c3.term_label, "A'")
        self.assertEqual(c3.Omega, 0)
        self.assertEqual(c3.html, "A'<sup>1</sup>A<sub>1g</sub><sub>0</sub>")
        self.assertEqual(c3.latex, "A'{}^{1}A_{1g}{}_{0}")

        c4 = MolecularTermSymbol('1E"1')
        self.assertEqual(c4.html, '<sup>1</sup>E"<sub>1</sub>')

        c5 = MolecularTermSymbol("1Σ+u")
        self.assertEqual(c5.html, "<sup>1</sup>Σ<sup>+</sup><sub>u</sub>")
        self.assertEqual(c5.latex, r"{}^{1}\Sigma^+_{u}")

        c6 = MolecularTermSymbol("1Σ-g")
        self.assertEqual(c6.html, "<sup>1</sup>Σ<sup>-</sup><sub>g</sub>")
        self.assertEqual(c6.latex, r"{}^{1}\Sigma^-_{g}")

    def test_greek_letter_conversion(self):
        m1 = MolecularTermSymbol("1SIGMA-")
        self.assertEqual(m1.Smult, 1)
        self.assertEqual(m1.irrep, "Σ-")
        self.assertEqual(str(m1), "1Σ-")

        m2 = MolecularTermSymbol("2PI")
        self.assertEqual(m2.Smult, 2)
        self.assertEqual(m2.irrep, "Π")
        self.assertEqual(str(m2), "2Π")
        self.assertEqual(m2.html, "<sup>2</sup>Π")

        m3 = MolecularTermSymbol("3SIGMA+u")
        self.assertEqual(m3.Smult, 3)
        self.assertEqual(m3.irrep, "Σ+u")
        self.assertEqual(str(m3), "3Σ+u")
        self.assertEqual(m3.html, "<sup>3</sup>Σ<sup>+</sup><sub>u</sub>")

        m3 = MolecularTermSymbol("4GAMMA")
        self.assertEqual(m3.Smult, 4)
        self.assertEqual(m3.irrep, "Γ")
        self.assertEqual(str(m3), "4Γ")
        self.assertEqual(m3.html, "<sup>4</sup>Γ")

        m3 = MolecularTermSymbol("2GAMMAg")
        self.assertEqual(m3.Smult, 2)
        self.assertEqual(m3.irrep, "Γg")
        self.assertEqual(str(m3), "2Γg")
        self.assertEqual(m3.html, "<sup>2</sup>Γ<sub>g</sub>")

        m3 = MolecularTermSymbol('A(1A")')
        self.assertEqual(str(m3), 'A(1A")')
        self.assertEqual(m3.html, 'A<sup>1</sup>A"')

        self.assertRaises(MolecularTermSymbolError, MolecularTermSymbol, 'A(A")')
        self.assertRaises(MolecularTermSymbolError, MolecularTermSymbol, "3B_2A")

    def test_molecular_term_symbol_equality(self):
        m1 = MolecularTermSymbol("1Σ+u")
        m2 = MolecularTermSymbol("1SIGMA+u")
        m3 = MolecularTermSymbol("X(1Σ+u)")

        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)

        m4 = MolecularTermSymbol("b(4Π_-3/2)")
        m5 = MolecularTermSymbol("b(4PI_-3/2)")
        m6 = MolecularTermSymbol("b(4Π)")
        self.assertEqual(m4, m5)
        self.assertNotEqual(m4, m6)

    def test_molecular_term_symbol_quantum_labels(self):
        c2 = MolecularTermSymbol("b(4Πu_-3/2)")
        self.assertEqual(c2.term_label, "b")
        self.assertEqual(c2.S, 1.5)
        self.assertEqual(c2.irrep, "Πu")
        self.assertEqual(c2.Omega, -1.5)

    def test_molecular_term_symbol_repr(self):
        m1 = MolecularTermSymbol("1Σ+u")
        m2 = MolecularTermSymbol("1SIGMA+u")
        self.assertTrue(repr(m1) == repr(m2) == "1Σ+u")

        m3 = MolecularTermSymbol("4Δ")
        m4 = MolecularTermSymbol("4DELTA")
        self.assertTrue(repr(m3) == repr(m4) == "4Δ")

    def test_term_symbol_label(self):
        m1 = MolecularTermSymbol("1(2B1)")
        self.assertEqual(repr(m1), "1(2B1)")
        self.assertEqual(m1.term_label, "1")
        self.assertRaises(MolecularTermSymbolError, MolecularTermSymbol, "1'(A\")")
        self.assertRaises(MolecularTermSymbolError, MolecularTermSymbol, '-2(A")')


if __name__ == "__main__":
    unittest.main()
