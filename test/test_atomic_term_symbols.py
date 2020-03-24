"""
Unit tests for the atomic term symbols module of PyValem
"""

import unittest

from pyvalem.state import StateParseError
from pyvalem.atomic_term_symbol import AtomicTermSymbol, AtomicTermSymbolError

class AtomicTermSymbolTest(unittest.TestCase):

    def test_atomic_term_symbol(self):
        a0 = AtomicTermSymbol('3P_1/2')
        self.assertEqual(a0.html, '<sup>3</sup>P<sub>1/2</sub>')
        # The quantum numbers: NB since these are half-integral, they can
        # be tested with assertEqual instead of assertAlmostEqual
        self.assertEqual(a0.S, 1.)
        self.assertEqual(a0.L, 1)
        self.assertEqual(a0.J, 0.5)

        a0 = AtomicTermSymbol('1S_0')
        self.assertEqual(a0.html, '<sup>1</sup>S<sub>0</sub>')
        self.assertEqual(a0.latex, '{}^{1}S_{0}')
        self.assertEqual(a0.S, 0)
        self.assertEqual(a0.L, 0)
        self.assertEqual(a0.J, 0)

        a1 = AtomicTermSymbol('4D')
        self.assertEqual(a1.html, '<sup>4</sup>D')
        self.assertEqual(a1.latex, '{}^{4}D')
        self.assertEqual(a1.S, 1.5)
        self.assertEqual(a1.L, 2)
        self.assertIsNone(a1.J)

        a2 = AtomicTermSymbol('2Po_1/2')
        self.assertEqual(a2.html, '<sup>2</sup>P<sup>o</sup><sub>1/2</sub>')
        self.assertEqual(a2.latex, '{}^{2}P^o_{1/2}')
        self.assertEqual(a2.parity, 'o')
        self.assertEqual(a2.L, 1)

        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, '1P_0')
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, '2PI')
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, '2PI_1/2')
        self.assertRaises(AtomicTermSymbolError, AtomicTermSymbol, '1PZ')

    def test_atomic_term_symbol_equality(self):
        a0 = AtomicTermSymbol('3P_1/2')
        a1 = AtomicTermSymbol('3P_1/2')
        a2 = AtomicTermSymbol('3P_3/2')
        self.assertEqual(a0, a1)
        self.assertNotEqual(a0, a2)
        


if __name__ == '__main__':
    unittest.main()


