"""
A State class, representing a quantum state or label of a species.

This is an abstract base class and specific types of state derive from it: use
one of those and don't instantiate State objects directly.
"""

from abc import ABC, abstractmethod
import html


class StateError(Exception):
    """A base class for state related exceptions."""

    pass


class StateParseError(StateError):
    """A base class for state parsing related exceptions."""

    pass


# noinspection PyUnresolvedReferences
class State(ABC):
    multiple_allowed = False

    @property
    def html(self):
        """HTML representation of the State instance.

        Returns
        -------
        str
        """
        return html.escape(repr(self))

    @property
    def latex(self):
        """LaTeX representation of the State instance.

        Returns
        -------
        str
        """
        return repr(self)

    @abstractmethod
    def __repr__(self):
        """In the context of PyValem package, the __repr__ method is overloaded to
        provide a *canonicalised* string representation of the structure. The
        main idea is that two objects which represent *the same* physical entity will
        have the same ``repr(obj)`` representation.
        """
        raise NotImplementedError

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

    @property
    def ordering(self):
        return repr(self)
