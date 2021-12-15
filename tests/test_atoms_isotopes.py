"""
Unit tests for the atom_data module of PyValem.
"""

import unittest

from pyvalem.atom_data import Atom, Isotope, atoms, isotopes

class AtomTest(unittest.TestCase):

    def test_atom_equality(self):
        carbon_atom = atoms['C']
        self.assertEqual(carbon_atom, Atom('C', 'carbon', 6))
        self.assertEqual(carbon_atom, 'C')
        self.assertNotEqual(carbon_atom, atoms['Co'])
        self.assertNotEqual(carbon_atom, 'Co')

        carbon13_atom = isotopes['13C']
        self.assertEqual(carbon13_atom, Isotope(6, 7, '13C', None, None, None))
        self.assertEqual(carbon13_atom, '13C')
        self.assertNotEqual(carbon13_atom, isotopes['59Co'])
        self.assertNotEqual(carbon13_atom, isotopes['13B'])
        self.assertNotEqual(carbon13_atom, '13Co')


if __name__ == '__main__':
    unittest.main()
