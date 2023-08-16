"""
Unit tests for the atomic term symbols module of PyValem
"""

import unittest

from pyvalem.states.atomic_term_symbol import AtomicTermSymbol, AtomicTermSymbolError


class AtomicTermSymbolTest(unittest.TestCase):
    def test_atomic_term_symbol(self):
        a0 = AtomicTermSymbol("2P_1/2")
        self.assertEqual(a0.html, "<sup>2</sup>P<sub>1/2</sub>")
        # The quantum numbers: NB since these are half-integral, they can
        # be tested with assertEqual instead of assertAlmostEqual
        self.assertEqual(a0.S, 0.5)
        self.assertEqual(a0.L, 1)
        self.assertEqual(a0.J, 0.5)

        a0 = AtomicTermSymbol("1S_0")
        self.assertEqual(a0.html, "<sup>1</sup>S<sub>0</sub>")
        self.assertEqual(a0.latex, r"{}^{1}\mathrm{S}_{0}")
        self.assertEqual(a0.S, 0)
        self.assertEqual(a0.L, 0)
        self.assertEqual(a0.J, 0)

        a1 = AtomicTermSymbol("4D")
        self.assertEqual(a1.html, "<sup>4</sup>D")
        self.assertEqual(a1.latex, r"{}^{4}\mathrm{D}")
        self.assertEqual(a1.S, 1.5)
        self.assertEqual(a1.L, 2)
        self.assertIsNone(a1.J)

        a2 = AtomicTermSymbol("2Po_1/2")
        self.assertEqual(a2.html, "<sup>2</sup>P<sup>o</sup><sub>1/2</sub>")
        self.assertEqual(a2.latex, r"{}^{2}\mathrm{P}^o_{1/2}")
        self.assertEqual(a2.parity, "o")
        self.assertEqual(a2.L, 1)

        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, "1P_0")
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, "2PI")
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, "2PI_1/2")
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, "1PZ")

        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, "3P_3/2")

    def test_atomic_term_symbol_equality(self):
        a0 = AtomicTermSymbol("2P_1/2")
        a1 = AtomicTermSymbol("2P_1/2")
        a2 = AtomicTermSymbol("2P_3/2")
        self.assertEqual(a0, a1)
        self.assertNotEqual(a0, a2)

    def test_moore_label(self):
        a0 = AtomicTermSymbol("a5D")
        a1 = AtomicTermSymbol("z3Po")
        a2 = AtomicTermSymbol("2F")
        a3 = AtomicTermSymbol("e5D_4")
        self.assertEqual(a0.moore_label, "a")
        self.assertEqual(a1.moore_label, "z")
        self.assertEqual(a2.moore_label, "")
        self.assertEqual(a3.moore_label, "e")
        self.assertEqual(a0.html, "a<sup>5</sup>D")
        self.assertEqual(a0.latex, r"a{}^{5}\mathrm{D}")
        self.assertEqual(a1.latex, r"z{}^{3}\mathrm{P}^o")
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, "A5D")


if __name__ == "__main__":
    unittest.main()
