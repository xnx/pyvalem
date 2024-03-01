"""
Unit tests for the Racah symbols module of PyValem.
"""

import unittest

from pyvalem.states.racah_symbol import RacahSymbol


class RacahSymbolTest(unittest.TestCase):
    def test_racah_symbol(self):
        r0 = RacahSymbol("5s'[1/2]_1")
        self.assertEqual(r0.html, "5s'[1/2]<sub>1</sub>")
        self.assertEqual(r0.principal, 5)
        self.assertEqual(r0.orbital, "s'")
        self.assertEqual(r0.k_num, 1)
        self.assertEqual(r0.k_den, 2)
        self.assertEqual(r0.j_term, 1)

        r1 = RacahSymbol("3p[5/2]_2")
        self.assertEqual(repr(r1), "3p[5/2]_2")
        self.assertEqual(r1.html, "3p[5/2]<sub>2</sub>")
        self.assertEqual(r1.principal, 3)
        self.assertEqual(r1.orbital, "p")
        self.assertEqual(r1.k_num, 5)
        self.assertEqual(r1.k_den, 2)
        self.assertEqual(r1.j_term, 2)

        r2 = RacahSymbol("4d[3/2]")
        self.assertEqual(repr(r2), "4d[3/2]")
        self.assertEqual(r2.html, "4d[3/2]")
        self.assertEqual(r2.principal, 4)
        self.assertEqual(r2.orbital, "d")
        self.assertEqual(r2.k_num, 3)
        self.assertEqual(r2.k_den, 2)
        self.assertEqual(r2.j_term, None)
        self.assertEqual(r2.parity, "")

        r3 = RacahSymbol("3p[3/2]o_2")
        self.assertEqual(repr(r3), "3p[3/2]o_2")
        self.assertEqual(r3.html, "3p[3/2]<sup>o</sup><sub>2</sub>")
        self.assertEqual(r3.principal, 3)
        self.assertEqual(r3.orbital, "p")
        self.assertEqual(r3.k_num, 3)
        self.assertEqual(r3.k_den, 2)
        self.assertEqual(r3.j_term, 2)
        self.assertEqual(r3.parity, "o")


if __name__ == "__main__":
    unittest.main()
