"""
A module for parsing strings or sequences of strings into appropriate
State-like objects or sequences of such objects.
"""
from collections import OrderedDict

from .atomic_configuration import AtomicConfiguration
from .atomic_term_symbol import AtomicTermSymbol
from .diatomic_molecular_configuration import DiatomicMolecularConfiguration
from .generic_excited_state import GenericExcitedState
from .key_value_pair import KeyValuePair
from .molecular_term_symbol import MolecularTermSymbol
from .racah_symbol import RacahSymbol
from .rotational_state import RotationalState
from .state import StateParseError
from .vibrational_state import VibrationalState

# the following has two purposes: keys determine the order in which the
# states are parsed, and the values determine the sorting order of states
# for StatefulSpecies.__repr__.
STATES = OrderedDict(
    [
        (GenericExcitedState, 0),
        (AtomicConfiguration, 1),
        (AtomicTermSymbol, 2),
        (DiatomicMolecularConfiguration, 1),
        (MolecularTermSymbol, 2),
        (VibrationalState, 3),
        (RotationalState, 4),
        (RacahSymbol, 5),
        (KeyValuePair, 6),
    ]
)


def state_parser(s_state):
    """Parse s_state into an appropriate State-like object or list of such."""

    if not s_state:
        return None

    if not isinstance(s_state, str):
        # If we have a sequence of strings, parse them one by one into a list
        # of State-like objects.
        return [state_parser(s.strip()) for s in s_state]

    # Try to parse the string s_state into a State-like object by trying each
    # of the possible derived State classes one by one in a particular order.
    for StateClass in STATES:
        try:
            return StateClass(s_state)
        except StateParseError:
            pass

    raise StateParseError("Could not parse {}".format(s_state))
