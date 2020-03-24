"""
The VibrationalState class, representing a molecular vibrational state, with
methods for parsing a string into quantum numbers and labels, creating
an HTML representation of it, etc.
"""

import pyparsing as pp
from .state import State, StateParseError

integer = pp.Word(pp.nums)

vibrational_term = pp.Group(pp.Optional(integer.setResultsName('n'), default=1)
                        + pp.Or(('v', 'ν')) + integer.setResultsName('mode'))
vibrational_config = (vibrational_term + 
                      pp.ZeroOrMore(pp.Suppress('+') + vibrational_term) +
                      pp.StringEnd()).leaveWhitespace()

class VibrationalTerm:
    def __init__(self, n, mode):
        self.n = int(n)
        self.mode = int(mode)
    
    def __str__(self):
        return '{}ν{:d}'.format(self.n if self.n > 1 else '', self.mode)
    __repr__=__str__

    @property
    def html(self):
        return '{}ν<sub>{:d}</sub>'.format(self.n if self.n > 1 else '',
                                             self.mode)

    @property
    def latex(self):
        return '{}\\nu_{{{:d}}}'.format(self.n if self.n > 1 else '',
                                             self.mode)
    def __lt__(self, other):
        return self.mode < other.mode

class VibrationalStateError(StateParseError):
    pass

class VibrationalState(State):

    multiple_allowed = False

    def parse_state(self, state_str):

        self.state_str = state_str.replace(' ','')
        self.v = None
        self.polyatomic = False

        def get_v(s_v):
            if s_v in ('*', '**', '***'):
                self.polyatomic = None
                return s_v
            return int(s_v)

        try:
            if self.state_str.startswith('v='):
                self.v = get_v(self.state_str[2:])
            else:
                self.v = get_v(self.state_str)
                self.state_str = 'v={}'.format(state_str)
        except ValueError:
            self.polyatomic = True
            try:
                parse_results = vibrational_config.parseString(self.state_str)
            except pp.ParseException:
                raise VibrationalStateError('Invalid vibrational state'
                    ' configuration syntax: {0}'.format(self.state_str))

            self.terms = [VibrationalTerm(parsed_term['n'],parsed_term['mode'])
                                     for parsed_term in parse_results]
            self.terms.sort()

    def __repr__(self):
        if self.v is not None:
            return 'v={}'.format(self.v)
        return '+'.join([str(term) for term in self.terms])
    __str__ = __repr__
    
    @property
    def html(self):
        html_chunks = []
        if self.polyatomic:
            return ' + '.join([term.html for term in self.terms])
        return self.__str__()

    @property
    def latex(self):
        latex_chunks = []
        if self.polyatomic:
            return ' + '.join([term.latex for term in self.terms])
        return self.__str__()
