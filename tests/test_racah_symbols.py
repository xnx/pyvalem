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
        self.assertEqual(r1.html, "3p[5/2]<sub>2</sub>")
        self.assertEqual(r1.principal, 3)
        self.assertEqual(r1.orbital, "p")
        self.assertEqual(r1.k_num, 5)
        self.assertEqual(r1.k_den, 2)
        self.assertEqual(r1.j_term, 2)


if __name__ == "__main__":
    unittest.main()
