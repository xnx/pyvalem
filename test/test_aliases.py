"""
Test aliases functionality of PyValem.
"""

import unittest
from pyvalem.formula import Formula

class AliasTest(unittest.TestCase):

    def test_valid_aliases(self):
        f_D = Formula('D')
        f_2H = Formula('(2H)')
        self.assertEqual(str(f_D), 'D')
        self.assertEqual(f_D.mass, f_2H.mass)
        self.assertTrue('2H' in f_D.atoms)

        f_DT = Formula('DT')
        f_2H3H = Formula('(2H)(3H)')
        self.assertEqual(str(f_DT), 'DT')
        self.assertEqual(f_DT.mass, f_2H3H.mass)
        self.assertTrue('2H' in f_DT.atoms)
        self.assertTrue('3H' in f_DT.atoms)

    def test_alaises_dont_break_elements(self):
        f = Formula('Ti')
        self.assertTrue('Ti' in f.atoms)
        f = Formula('Dy')
        self.assertTrue('Dy' in f.atoms)
        f = Formula('DsD')
        self.assertTrue('2H' in f.atoms)
        self.assertTrue('Ds' in f.atoms)

if __name__ == '__main__':
    unittest.main()
