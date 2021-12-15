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

        f_Dminus = Formula('D-')
        self.assertEqual(str(f_Dminus), 'D-')
        self.assertTrue('2H' in f_Dminus.atoms)
        self.assertEqual(f_Dminus.natoms, 1)
        self.assertEqual(f_Dminus.charge, -1)
        
        f_Dminus2 = Formula('D-2')
        self.assertEqual(str(f_Dminus2), 'D-2')
        self.assertTrue('2H' in f_Dminus2.atoms)
        self.assertEqual(f_Dminus2.natoms, 1)
        self.assertEqual(f_Dminus2.charge, -2)

        f_Tplus = Formula('T+')
        self.assertEqual(str(f_Tplus), 'T+')
        self.assertTrue('3H' in f_Tplus.atoms)
        self.assertEqual(f_Tplus.natoms, 1)
        self.assertEqual(f_Tplus.charge, 1)


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
