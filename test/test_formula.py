"""
Unit tests for the formula module of PyValem
"""

import unittest

from pyvalem.formula import Formula, FormulaParseError
from good_formulas import good_formulas

class FormulaTest(unittest.TestCase):

    def test_stoichiometric_formula_test(self):
        cf = Formula('C2F4H2')
        self.assertEqual(cf.stoichiometric_formula(), 'H2C2F4')
        self.assertEqual(cf.stoichiometric_formula('alphabetical'), 'C2F4H2')
        #self.assertEqual(cf.stoichiometric_formula('hill'), 'C2H2F4')

        cf = Formula('CFx')
        self.assertEqual(cf.stoichiometric_formula(), 'CFx')

    def test_html_and_slug(self):
        f = (('NO+', 'NO+', 'NO<sup>+</sup>', 'NO_p'),
             ('OH-', 'HO-', 'OH<sup>-</sup>', 'OH_m'),
             ('CoN6H18-2', 'H18N6Co-2',
              'CoN<sub>6</sub>H<sub>18</sub><sup>2-</sup>',
              'CoN6H18_m2'),
             ('(14N)(1H)(16O)2(18O)(16O)', '(1H)(14N)(16O)3(18O)',
              '<sup>14</sup>N<sup>1</sup>H<sup>16</sup>O<sub>2</sub>'
                      '<sup>18</sup>O<sup>16</sup>O',
              '14N-1H-16O2-18O-16O'),
             ('CFx', 'CFx', 'CF<sub>x</sub>', 'CFx'),
             )

        for formula, stoich_formula, html, slug in f:
            cf = Formula(formula)
            self.assertEqual(cf.stoichiometric_formula(), stoich_formula)
            self.assertEqual(cf.html, html)
            self.assertEqual(cf.slug, slug)

    def test_moieties(self):
        cf = Formula('H2NC(CH3)2CO2H')
        self.assertEqual(cf.html, 'H<sub>2</sub>NC(CH<sub>3</sub>)'
                                  '<sub>2</sub>CO<sub>2</sub>H')
        self.assertEqual(cf.slug, 'H2NC-_l_CH3_r_2-CO2H')
        atom_symbols = {atom.symbol for atom in cf.atoms}
        self.assertEqual(atom_symbols, {'H', 'C', 'N', 'O'})

        cf = Formula('Co(H2O)6+2')
        self.assertEqual(cf.html,
                         'Co(H<sub>2</sub>O)<sub>6</sub><sup>2+</sup>')
        self.assertEqual(cf.slug, 'Co-_l_H2O_r_6_p2')

    def test_good_formulas(self):
        for formula in good_formulas:
            cf = Formula(formula)
            #print(formula)
            self.assertEqual(cf.stoichiometric_formula(),
                             good_formulas[formula]['stoichiometric_formula'])
            self.assertEqual(cf.html, good_formulas[formula]['html'])
            self.assertEqual(cf.slug, good_formulas[formula]['slug'])
            self.assertAlmostEqual(cf.rmm, good_formulas[formula]['rmm'])
            if 'natoms' in good_formulas[formula].keys():
                self.assertEqual(cf.natoms, good_formulas[formula]['natoms'])
            if 'latex' in good_formulas[formula].keys():
                self.assertEqual(cf.latex, good_formulas[formula]['latex']) 

    def test_Tc_Pm(self):
        for f in ('Tc', 'Pm', 'TcH', 'Cl2Pm'):
            cf = Formula(f)
            self.assertIsNone(cf.rmm)

    def test_charged_species(self):
        cf1 = Formula('H+')
        self.assertEqual(cf1.html, 'H<sup>+</sup>')
        self.assertEqual(cf1.charge, 1)

    def test_M(self):
        cf = Formula('M')
        self.assertEqual(cf.stoichiometric_formula(), 'M')
        self.assertEqual(cf.html, 'M')
        self.assertEqual(cf.slug, 'M')
        self.assertIsNone(cf.rmm)
        self.assertIsNone(cf.natoms)
        self.assertIsNone(cf.charge)
        self.assertEqual(cf.atoms, {'M'})

    def test_e(self):
        cf = Formula('e-')
        self.assertEqual(cf.stoichiometric_formula(), 'e-')
        self.assertEqual(cf.html, 'e<sup>-</sup>')
        self.assertEqual(cf.slug, 'e_m')
        self.assertEqual(cf.mass, 5.48579909e-04)
        self.assertIsNone(cf.natoms)
        self.assertEqual(cf.charge, -1)
        
    def test_photon(self):
        for cf in (Formula('hν'), Formula('hv')):
            self.assertEqual(cf.stoichiometric_formula(), 'hν')
            self.assertEqual(cf.slug, 'hv')
            self.assertEqual(cf.html, 'hν')
            self.assertEqual(cf.mass, 0)
            self.assertIsNone(cf.natoms)
            self.assertEqual(cf.charge, 0)

    def test_parse_fail(self):
        self.assertRaises(FormulaParseError, Formula, 'Mq')
        self.assertRaises(FormulaParseError, Formula, '(27N)')
        self.assertRaises(FormulaParseError, Formula, 'H3O^+')
        self.assertRaises(FormulaParseError, Formula, 'H_2S')
        

if __name__ == '__main__':
    unittest.main()

