"""
The KeyValuePair class, representing an arbitrary atomic or molecular state,
with methods for parsing it from a string and outputting its HTML
representation, etc.
"""
import html

from .state import State, StateParseError


class KeyValuePairError(StateParseError):
    pass


class KeyValuePair(State):
    """
    A class representing an state as an arbitrary key/value pair.

    Any atomic or molecular state that doesn't fit into any of the other
    explicit categories available in PyValem can be represented as a
    key/value pair, parsed in the form 'key=value'.
    """

    multiple_allowed = True

    def __init__(self, state_str):
        self.state_str = None
        self.key = None
        self.value = None
        self.parse_state(state_str)

    def parse_state(self, state_str):
        """
        Parse state_str into a KeyValuePair object.

        Whitespace is tolerated in the input, i.e both 'key=value' and
        'key = value' are parsed, but no spaces are inserted in the output.
        """
        try:
            key, value = state_str.split("=")
        except ValueError:
            raise KeyValuePairError("Invalid key-value pair: {}.".format(state_str))
        self.key = key.strip()
        self.value = value.strip()

        self.state_str = "{}={}".format(self.key, self.value)

    @property
    def html(self):
        return html.escape(str(self))
