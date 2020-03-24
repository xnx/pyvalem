"""
The AtomicTermSymbol class, representing an atomic term symbol, with
methods for parsing a string into quantum numbers and labels, creating
an HTML representation of the term symbol, etc.
"""

import pyparsing as pp
from .state import State, StateParseError
from .utils import parse_fraction, float_to_fraction

atom_L_symbols = ('S', 'P', 'D', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O',
                  'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

integer = pp.Word(pp.nums)

atom_Smult = integer.setResultsName('Smult')
atom_Lletter = pp.oneOf(atom_L_symbols).setResultsName('Lletter')
atom_Jstr = (integer+pp.Optional(pp.Suppress('/')+'2')+pp.StringEnd()
            ).setResultsName('Jstr')
atom_parity = pp.Literal('o').setResultsName('parity')
atom_term = (atom_Smult + atom_Lletter + pp.Optional(atom_parity) +
             pp.Optional(pp.Suppress('_') + atom_Jstr) + pp.StringEnd())

class AtomicTermSymbolError(StateParseError):
    pass

class AtomicTermSymbol(State):

    multiple_allowed = False

    def parse_state(self, state_str):
        self.state_str = state_str

        try:
            components = atom_term.parseString(state_str)
        except pp.ParseException:
            raise AtomicTermSymbolError('Invalid atomic term symbol syntax:'
                                        ' {0}'.format(state_str))
        self.Smult = int(components.Smult)
        self.S = (self.Smult - 1) / 2.
        self.Lletter = components.Lletter
        self.L = atom_L_symbols.index(components.Lletter)
        self.parity = components.get('parity')
        try:
            self.J = parse_fraction(components.Jstr)
        except ValueError as err:
            raise AtomicTermSymbolError(err)
        if self.J is not None:
            self.validate_J()
                
    def validate_J(self):
        if not abs(self.L - self.S) <= self.J <= self.L + self.S:
            raise AtomicTermSymbolError('Invalid atomic term symbol: {0:s}'
                ' |L-S| <= J <= L+S must be satisfied.'.format(self.state_str))

    @property
    def html(self):
        html_chunks = ['<sup>{0:d}</sup>{1:s}'.format(self.Smult,self.Lletter)]
        if self.parity:
            html_chunks.append('<sup>o</sup>')
        if self.J is not None:
            Jstr = float_to_fraction(self.J)
            html_chunks.append('<sub>{0:s}</sub>'.format(Jstr))
        return ''.join(html_chunks)

    @property
    def latex(self):
        latex_chunks = ['{{}}^{{{}}}{}'.format(self.Smult, self.Lletter)]
        if self.parity:
            latex_chunks.append('^o')
        if self.J is not None:
            Jstr = float_to_fraction(self.J)
            latex_chunks.append('_{{{}}}'.format(Jstr))
        return ''.join(latex_chunks)
