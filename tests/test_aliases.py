"""
Test aliases functionality of PyValem.
"""

import unittest

from pyvalem.formula import Formula


class AliasTest(unittest.TestCase):
    def test_valid_aliases(self):
        f_d = Formula("D")
        f_2h = Formula("(2H)")
        self.assertEqual(str(f_d), "D")
        self.assertEqual(f_d.mass, f_2h.mass)
        self.assertTrue("2H" in f_d.atoms)

        f_dt = Formula("DT")
        f_2h3h = Formula("(2H)(3H)")
        self.assertEqual(str(f_dt), "DT")
        self.assertEqual(f_dt.mass, f_2h3h.mass)
        self.assertTrue("2H" in f_dt.atoms)
        self.assertTrue("3H" in f_dt.atoms)

        f_d_m = Formula("D-")
        self.assertEqual(str(f_d_m), "D-")
        self.assertTrue("2H" in f_d_m.atoms)
        self.assertEqual(f_d_m.natoms, 1)
        self.assertEqual(f_d_m.charge, -1)

        f_d_m2 = Formula("D-2")
        self.assertEqual(str(f_d_m2), "D-2")
        self.assertTrue("2H" in f_d_m2.atoms)
        self.assertEqual(f_d_m2.natoms, 1)
        self.assertEqual(f_d_m2.charge, -2)

        f_t_p = Formula("T+")
        self.assertEqual(str(f_t_p), "T+")
        self.assertTrue("3H" in f_t_p.atoms)
        self.assertEqual(f_t_p.natoms, 1)
        self.assertEqual(f_t_p.charge, 1)

    def test_alaises_dont_break_elements(self):
        f = Formula("Ti")
        self.assertTrue("Ti" in f.atoms)
        f = Formula("Dy")
        self.assertTrue("Dy" in f.atoms)
        f = Formula("DsD")
        self.assertTrue("2H" in f.atoms)
        self.assertTrue("Ds" in f.atoms)


if __name__ == "__main__":
    unittest.main()
