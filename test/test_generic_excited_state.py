"""
Unit tests for the generic_excited_state module of PyValem
"""

import unittest

from pyvalem.generic_excited_state import (GenericExcitedState,
                                           GenericExcitedStateError)

class GenericExcitedStateTest(unittest.TestCase):
    def test_generic_excited_term_symbol(self):
        x0 = GenericExcitedState('*')
        self.assertEqual(x0.html, '<sup>*</sup>')
        x1 = GenericExcitedState('**')
        self.assertEqual(x1.html, '<sup>**</sup>')
        x2 = GenericExcitedState('***')
        self.assertEqual(x2.html, '<sup>***</sup>')
        
        x3 = GenericExcitedState('3*')
        self.assertEqual(x3.int_n,3)
        self.assertEqual(x3.html, '3<sup>*</sup>')
        
        x4 = GenericExcitedState('15*')
        self.assertEqual(x4.int_n,15)
        self.assertEqual(x4.html, '15<sup>*</sup>')
        
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, 'a')
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, '*3')
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, '3 *')
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, '3**')
        self.assertRaises(GenericExcitedStateError,GenericExcitedState, '3**?')
        self.assertRaises(GenericExcitedStateError,GenericExcitedState, '*4**')


if __name__ == '__main__':
    unittest.main()
