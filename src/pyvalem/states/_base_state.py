"""
A State class, representing a quantum state or label of a species.

This is an abstract base class and specific types of state derive from it: use
one of those and don't instantiate State objects directly.
"""

import html
from abc import ABC, abstractmethod

from pyvalem.exceptions import PyValemError


class StateError(PyValemError):
    """A base class for state related exceptions."""

    pass


class StateParseError(StateError):
    """A base class for state parsing related exceptions."""

    pass


# noinspection PyUnresolvedReferences
class State(ABC):
    multiple_allowed = False

    def __new__(cls, state_str, *args, **kwargs):
        if not isinstance(state_str, str):
            raise TypeError(
                "{} must be created from a str, not {}".format(
                    cls.__name__, type(state_str).__name__
                )
            )
        return super().__new__(cls)

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
        if not isinstance(other, State):
            return NotImplemented
        return isinstance(other, self.__class__) and repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))

    @property
    def ordering(self):
        return repr(self)
