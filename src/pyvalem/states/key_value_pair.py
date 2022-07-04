"""
The KeyValuePair class, representing an arbitrary atomic or molecular state,
with methods for parsing it from a string and outputting its HTML
representation, etc.
"""
from pyvalem.states._base_state import State, StateParseError


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
        self._parse_state(state_str)

    def _parse_state(self, state_str):
        """
        Parse state_str into a KeyValuePair object.

        Whitespace is not tolerated in the input, i.e only 'key=value' and not
        'key = value' are allowed. No spaces are inserted in the output.
        """

        if any(c.isspace() for c in state_str):
            raise KeyValuePairError(
                "No whitespace allowed in key-value pair: {}".format(state_str)
            )

        try:
            key, value = state_str.split("=")
        except ValueError:
            raise KeyValuePairError("Invalid key-value pair: {}.".format(state_str))
        self.key = key.strip()
        self.value = value.strip()

        self.state_str = "{}={}".format(self.key, self.value)

    def __repr__(self):
        return self.state_str

    @property
    def ordering(self):
        if self.key == "n":
            # Move up n to the first position for ordering by replacing it with
            # a space (ASCII 32, the first printable character and not a real valid
            # key.
            return " "
        return self.key
