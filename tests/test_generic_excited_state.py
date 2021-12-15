"""
Unit tests for the generic_excited_state module of PyValem
"""

import unittest

from pyvalem.generic_excited_state import (GenericExcitedState,
                                           GenericExcitedStateError)

class GenericExcitedStateTest(unittest.TestCase):
    def test_generic_excited_state_html(self):
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

    def test_generic_excited_state_repr(self):
        x1a = GenericExcitedState('*')
        x1b = GenericExcitedState('1*')
        x2a = GenericExcitedState('**')
        x2b = GenericExcitedState('2*')
        x3a = GenericExcitedState('***')
        x3b = GenericExcitedState('3*')
        x4a = GenericExcitedState('****')
        x4b = GenericExcitedState('4*')
        self.assertEqual(repr(x1a), repr(x1b), '*')
        self.assertEqual(repr(x2a), repr(x2b), '**')
        self.assertEqual(repr(x3a), repr(x3b), '3*')
        self.assertEqual(repr(x4a), repr(x4b), '4*')


if __name__ == '__main__':
    unittest.main()
