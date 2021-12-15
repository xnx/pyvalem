# state.py
# Version 1.2
# A base class representing an atomic or molecular state.
# Various derived classes will create their versions of State
# objects by parsing text strings.
#
# Copyright (C) 2012-2016 Christian Hill
# xn.hill@gmail.com
"""
A State class, representing a quantum state or label of a species.

This is an abstract base class and specific types of state derive from it: use
one of those and don't instantiate State objects directly.
"""


class StateError(Exception):
    pass


class StateParseError(StateError):
    pass


# noinspection PyUnresolvedReferences
class State:
    multiple_allowed = False

    def __repr__(self):
        return self.state_str

    @property
    def html(self):
        return str(self)

    @property
    def latex(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.__repr__() == other.__repr__():
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())
